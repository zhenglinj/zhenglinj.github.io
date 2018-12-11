# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from ftptool import FTPHost

# ftp://ftp.gnu.org/
a_host = FTPHost.connect("ftp://ftp.gnu.org/", user="anonymous", password="", timeout=1000)

a_host.current_directory = "/"

for (dirname, subdirs, files) in a_host.walk("/"):
    for subdir in subdirs:
        if subdir.startswith("other_"):
            subdirs.remove(subdir)
    print(dirname, "has file(s)", ", ".join(files))

# print tree
def FtpWalker(dirname, prefix = ""):
    a_host.current_directory = dirname
    (subdirs, files) = a_host.listdir(dirname)
    print(prefix, dirname, ": ", ", ".join(files), sep="")
    for subdir in subdirs:
        FtpWalker(dirname+"/"+subdir, prefix = prefix+"\t")

FtpWalker("/")

# Local Variables:
# python-shell-interpreter: "python"
# flycheck-checker: python-flake8-py2
# End:
