#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
./find4ftp.py /gnu/apl/ --ftpurl ftp.gnu.org --name ".*\\.tar\\.gz" --type f --depth 2
./find4ftp.py /gnu/apl/ --ftpurl ftp.gnu.org --name "(.*)-(.*)(\\.tar\\.gz)" --type f --evalprint "m.group(1)+'-{version}'+m.group(3)"
"""

from __future__ import print_function

import ftplib
import os
import posixpath
import re
import socket
from argparse import ArgumentParser
from functools import partial
from os import path

import six


def _parse_list_line(line, files=[], subdirs=[], links=None):
    """Parse *line* and insert into either *files* or *subdirs* depending on
    whether the line is for a directory or not.
    This is used as the callback to the ftplib.FTPConnection.dir callback.
    """
    dst = None
    if line.startswith("d"):
        dst = subdirs
    elif line.startswith("-"):
        dst = files
    elif line.startswith("l"):
        dst = links
    else:
        raise ValueError("unknown line type %r" % line[:1])
    # No dst set for this type: ignore.
    if dst is None:
        return
    parts = line.split(None, 8)
    stat, name = parts[0], parts[-1]
    dst.append(name)

class FTPHost(object):
    """Represent a connection to a remote host.
    A remote host has a working directory, and an ftplib object connected.
    """

    def __init__(self, ftp_obj):
        """Initialize with a ftplib.FTP instance (or an instance of a
        subclass). Use the classmethod connect to create an actual ftplib
        connection and get an FTPHost instance.
        """
        self.ftp_obj = ftp_obj

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.ftp_obj)

    def __str__(self):
        return "<%s at %s:%d (%s)>" % (self.__class__.__name__,
            self.ftp_obj.host, self.ftp_obj.port, self.ftp_obj)

    @classmethod
    def connect(cls, host, port=21, user=None, password=None, account=None,
                ftp_client=ftplib.FTP, debuglevel=0, timeout=None):
        """Connect to host, using port. If user is given, login with given
        user, password and account. The two latter can be None, in which case
        ftplib will set the password to 'anonymous@'. You can choose which
        class to instance by means of ftp_client.
        """
        ftp_obj = ftp_client()
        ftp_obj.set_debuglevel(debuglevel)
        if timeout is not None:
            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(float(timeout))
            ftp_obj.connect(host, port)
            socket.setdefaulttimeout(old_timeout)
        else:
            ftp_obj.connect(host, port)

        # And log in.
        if user:
            ftp_obj.login(user, password, account)
        return cls(ftp_obj)

    def file_proxy(self, filename):
        """Creates a file proxy object for filename. See FTPFileProxy."""
        return FTPFileProxy(self.ftp_obj,
            posixpath.join(self.current_directory, filename))

    def get_current_directory(self):
        if not hasattr(self, "_cwd"):
            self._cwd = self.ftp_obj.pwd()
        return self._cwd

    def set_current_directory(self, directory):
        self.ftp_obj.cwd(directory)
        self._cwd = self.ftp_obj.pwd()

    current_directory = property(get_current_directory, set_current_directory)

    def mkdir(self, directory):
        """Make directory."""
        self.ftp_obj.mkd(directory)

    def rmdir(self, directory):
        """Remove directory."""
        self.ftp_obj.rmd(directory)

    def walk(self, directory):
        """Emulates os.walk very well, even the caveats."""
        (subdirs, files) = self.listdir(directory)
        # Yield value.
        yield (directory, subdirs, files)
        # Recurse subdirs.
        for subdir in subdirs:
            for x in self.walk(posixpath.join(directory, subdir)):
                yield x

    def listdir(self, directory, links=False):
        """Returns a list of files and directories at `directory`, relative to
        the current working directory. The return value is a two-tuple of
        (dirs, files).
        """
        directory = directory.rstrip("/")
        kwds = dict(files=[], subdirs=[])
        if links:
            kwds["links"] = []
        cb = partial(_parse_list_line, **kwds)
        self.ftp_obj.dir(directory, cb)
        if links:
            return (kwds["subdirs"], kwds["files"], kwds["links"])
        else:
            return (kwds["subdirs"], kwds["files"])

    def mirror_to_local(self, source, destination):
        """Download remote directory found by source to destination."""
        # Cut off excess slashes.
        source = source.rstrip("/")
        destination = destination.rstrip("/")

        for current_dir, subdirs, files in self.walk(source):
            # current_destination will be the destination directory, plus the
            # current subdirectory. Have to treat the empty string separately,
            # because otherwise we'd be skipping a byte of current_dir,
            # because of the +1, which is there to remove a slash.
            if source:
                current_destination = path.join(destination,
                    current_dir[len(source) + 1:])
            else:
                current_destination = path.join(destination, current_dir)
            # Create all subdirectories lest they exist.
            for subdir in subdirs:
                subdir_full = path.join(current_destination, subdir)
                if not path.exists(subdir_full):
                    os.mkdir(subdir_full)
            # Download all files in current directory.
            for filename in files:
                target_file = path.join(current_destination, filename)
                remote_file = posixpath.join(source, current_dir, filename)
                self.file_proxy(remote_file).download_to_file(target_file)

    def mirror_to_remote(self, source, destination, create_destination=False,
            ignore_dotfiles=True):
        """Upload local directory `source` to remote destination `destination`.
        Create destination directory only if `create_destination` is True, and
        don't upload or descend into files or directories starting with a dot
        if `ignore_dotfiles` is True.
        """
        # Cut off excess slashes.
        source = source.rstrip("/")
        destination = destination.rstrip("/")

        if ignore_dotfiles and \
                any(part.startswith(".") for part in destination.split("/")):
            raise ValueError("cannot have a destination with dots when "
                "ignore_dotfiles is True")

        # Create remote FTP destination
        if create_destination:
            try:
                self.makedirs(destination)
            except ftplib.Error:
                pass

        for current_dir, subdirs, files in os.walk(source):
            # Current remote destination = destination dir + current.
            # See mirror_to_local for the census of special-casing the empty
            # string.
            if source:
                remote_dest_dir = posixpath.join(destination,
                    current_dir[len(source) + 1:])
            else:
                remote_dest_dir = posixpath.join(destination, current_dir)

            # Clean subdirs & files from dotfiles if wanted - some FTP daemons
            # hate dotfiles.
            if ignore_dotfiles:
                # Copy the list, and remove dotfiles and dirs from the real
                # list. We need to use remove and not some shady filter
                # because otherwise we'll walk into dotdirs and defeat the
                # purpose of the parameter.
                for subdir in subdirs[:]:
                    if subdir.startswith("."):
                        subdirs.remove(subdir)
                for filename in files[:]:
                    if filename.startswith("."):
                        files.remove(filename)

            # Create all directories required.
            for subdir in subdirs:
                # Ignore FTP exceptions here because if they're fatal, we'll
                # get it later when we upload.
                try:
                    self.mkdir(posixpath.join(remote_dest_dir, subdir))
                except ftplib.Error:
                    pass

            # Upload all files.
            for filename in files:
                local_source_file = path.join(current_dir, filename)
                remote_dest_file = posixpath.join(remote_dest_dir, filename)
                f = self.file_proxy(remote_dest_file)
                f.upload_from_file(local_source_file)

    def makedirs(self, dpath):
        """Try to create directories out of each part of `dpath`.
        First tries to change directory into `dpath`, to see if it exists. If
        it does, returns immediately. Otherwise, splits `dpath` up into parts,
        trying to create each accumulated part as a directory.
        """
        # First try to chdir to the target directory, to skip excess attempts
        # at directory creation. XXX: Probably should try full path, then cut
        # off a piece and try again, recursively.
        pwd = self.current_directory
        try:
            self.current_directory = dpath
        except ftplib.Error:
            pass
        else:
            return
        finally:
            self.current_directory = pwd
        # Then if we're still alive, split the path up.
        parts = dpath.split(posixpath.sep)
        # Then iterate through the parts.
        cdir = ""
        for dir in parts:
            cdir += dir + "/"
            # No point in trying to create the directory again when we only
            # added a slash.
            if not dir:
                continue
            try:
                self.mkdir(cdir)
            except ftplib.Error:
                pass

    def quit(self):
        """Send quit command and close connection."""
        self.ftp_obj.quit()

    def close(self):
        """Close connection ungracefully."""
        self.ftp_obj.close()

    def try_quit(self):
        """Attempt a quit, always close."""
        try:
            self.quit()
        except:
            self.close()

class FTPFileClient(FTPHost):
    """Class for emulating an FTP client, that is, get & put files to and from.
    """

    def _apply_all(self, filenames, f):
        rs = []
        for filename in filenames:
            source, destination = filename, path.basename(filename)
            rs.append(f(source, destination))
        return rs

    def get(self, source, destination):
        return self.file_proxy(source).download_to_file(destination)

    def put(self, source, destination):
        return self.file_proxy(destination).upload_from_file(source)

    def delete(self, filename):
        return self.file_proxy(filename).delete()

    # {{{ m*
    def mget(self, filenames):
        return self._apply_all(self.get, filenames)

    def mput(self, filenames):
        return self._apply_all(self.put, filenames)

    def mdelete(self, filenames):
        return self._apply_all(self.delete, filenames)
    # }}}

class ExtensionMappedFTPHost(FTPHost):
    """Takes a mapping of extensions to rewrite to another extension.  An
    extension is defined as "the bytes after the last dot". The mapping should
    have keys _without_ a dot, and so should the value. The value can be set to
    the empty string, and the end result will _not_ have a trailing dot.
    """

    @classmethod
    def connect(cls, *a, **kw):
        extension_map = kw.pop("extension_map", {})
        self = super(ExtensionMappedFTPHost, cls).connect(*a, **kw)
        self.extension_map = extension_map
        return self

    def file_proxy(self, filename):
        for key in self.extension_map:
            if filename.endswith("." + key):
                # Remove old extension.
                filename = filename[:-len(key) - 1]
                # Add the new.
                new_extension = self.extension_map[key]
                if new_extension:
                    filename += "." + new_extension
                break
        return super(ExtensionMappedFTPHost, self).file_proxy(filename)

class FTPFileProxy(object):
    def __init__(self, ftp_obj, filename):
        """Initialize file an ftplib.FTPConnection, and filename."""
        self.ftp_obj = ftp_obj
        self.filename = filename

    def upload(self, fp):
        """Uploadad file from file-like object fp."""
        self.ftp_obj.storbinary("STOR %s" % (self.filename,), fp)

    def upload_from_str(self, v):
        """Upload file from contents in string v."""
        self.upload(six.BytesIO(v))

    def upload_from_file(self, filename):
        """Upload file from file identified by name filename."""
        fp = file(filename, "rb")
        try:
            self.upload(fp)
        finally:
            fp.close()

    def download(self, fp):
        """Download file into file-like object fp."""
        self.ftp_obj.retrbinary("RETR %s" % (self.filename,), fp.write)

    def download_to_str(self):
        """Download file and return its contents."""
        fp = six.BytesIO()
        self.download(fp)
        return fp.getvalue()

    def download_to_file(self, filename):
        """Download file into file identified by name filename."""
        fp = file(filename, "wb")
        try:
            self.download(fp)
        finally:
            fp.close()

    def delete(self):
        """Delete file."""
        self.ftp_obj.delete(self.filename)

    def rename(self, new_name):
        """Rename file to new_name, and return an instance of that file."""
        new_abs_name = posixpath.join(path.dirname(self.filename), new_name)
        self.ftp_obj.rename(self.filename, new_abs_name)
        return self.__class__(self.ftp_obj, new_abs_name)



class BColors:
    """
    格式：\033[显示方式;前景色;背景色m
    说明：
    前景色            背景色           颜色
    ---------------------------------------
    30                40              黑色
    31                41              红色
    32                42              绿色
    33                43              黃色
    34                44              蓝色
    35                45              紫红色
    36                46              青蓝色
    37                47              白色
    显示方式           意义
    -------------------------
    0                终端默认设置
    1                高亮显示
    4                使用下划线
    5                闪烁
    7                反白显示
    8                不可见
    例子：
    \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
    \033[0m          <!--采用终端默认设置，即取消颜色设置-->
    """
    ENDC = '\033[0m'

    @staticmethod
    def C(highlight_cd, front_cd, back_cd):
     result = '\033[' + str(highlight_cd) + ';'
     result += str({ "B": 30, "r": 31, "g": 32, "y": 33, "b": 34, "m": 35, "a": 36, "w": 37, "": 99 }[front_cd]) + ';'
     result += str({ "B": 40, "r": 41, "g": 42, "y": 43, "b": 44, "m": 45, "a": 46, "w": 47, "": 99 }[back_cd]) + 'm'
     return result


def FindInFtp(a_host, startdir, spec_type, maxdepth, name_pat, eval_print, color):
    def WalkFtp(startdir, spec_type, maxdepth):
        if (maxdepth is None):
            pass
        elif ((type(maxdepth) is int) and maxdepth > 0):
            maxdepth = maxdepth-1
        else:
            return
        a_host.current_directory = startdir
        subdirs, files, links = a_host.listdir(startdir, True)
        last_xs = []
        if (spec_type is None or spec_type == "f"):
            for fn in files:
                mat = name_pattern.match(fn)
                if (mat):
                    EvalPrint(startdir, fn, last_xs, mat, eval_print)
        if (spec_type is None or spec_type == "l"):
            for l in links:
                mat = name_pattern.match(l)
                if (mat):
                    EvalPrint(startdir, l, last_xs, mat, eval_print)
        for sd in subdirs:
            if (sd == "." or sd == ".."):
                continue
            mat = name_pattern.match(sd)
            if ((spec_type is None or spec_type == "d") and mat):
                EvalPrint(startdir, sd, last_xs, mat, eval_print)
            WalkFtp(posixpath.join(startdir, sd), spec_type, maxdepth)

    def EvalPrint(startdir, x, last_xs, m, eval_print):
        try:
            newx = eval(eval_print)
        except Exception as ex:
            print("Eval print statements error: {0}".format(ex.strerror))
        if (newx not in last_xs):
            print(posixpath.join(startdir, BColors.C(0, "r", "") + newx + BColors.ENDC)) if color else print(posixpath.join(startdir, newx))
            last_xs.append(newx)

    try:
        name_pat = name_pat if (name_pat.endswith("\Z")) else "(?:"+name_pat+")\Z"
        name_pattern = re.compile(name_pat)
    except Exception as ex:
        print("RE compile error: {0}".format(ex.strerror))
    WalkFtp(startdir, spec_type, maxdepth)


if __name__ == "__main__":
    parser = ArgumentParser(description="The Ftp Find version like UNIX 'find' command")
    parser.add_argument("--ftpurl", type=str, required=True,
                        help="ftp URL")
    parser.add_argument("--ftpusr", type=str, default="anonymous",
                        help="ftp username")
    parser.add_argument("--ftppw", type=str, default="",
                        help="ftp password")
    parser.add_argument("startdir", type=str, default="/",
                        help="current work directory")
    parser.add_argument("--type", choices=["f", "d"], default=None,
                        help="type ((f)ile, (d)irectory), default all")
    parser.add_argument("--maxdepth", type=int, default=None,
                        help="descend at most n directory levels below the command line arguments")
    parser.add_argument("--name", default=".*",
                        help="name pattern, support python style regex")
    parser.add_argument("--evalprint", type=str, default="m.group(0)",
                        help="eval print, embed python print content, default like: m.group(0)")
    parser.add_argument("--color", action="store_true",
                        help="colorfull print if enabled")
    parser.add_argument("--debug", action="store_true",
                        help="print debug info if enabled")
    options = parser.parse_args()
    if (options.debug):
        print(options)

    a_host = FTPHost.connect(options.ftpurl, user=options.ftpusr, password=options.ftppw)
    FindInFtp(a_host, options.startdir, options.type, options.maxdepth, options.name, options.evalprint, options.color)
