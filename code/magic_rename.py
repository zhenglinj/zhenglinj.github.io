#!/usr/bin/env python

from __future__ import print_function
from argparse import ArgumentParser
import os
import base64

def Rename(fromname, is_decode):
    toname = ""
    if is_decode:
        toname = base64.b64decode(fromname, "+-")
        print("    ", fromname, "->", toname)
        os.rename(fromname, toname)
    else:
        toname = base64.b64encode(fromname, "+-")
        print("    ", fromname, "->", toname)
        os.rename(fromname, toname)
    return toname

def ErgodicDir(root_dir, prev_dir=""):
    if not os.path.isdir(root_dir):
        raise ValueError("The 1st argument should be directory")
    list_dir = os.listdir(root_dir)
    os.chdir(root_dir)
    for filename in list_dir:
        print(os.path.join(prev_dir, root_dir, filename))
        if os.path.isdir(filename):
            ErgodicDir(filename, os.path.join(prev_dir, root_dir))
            Rename(filename, options.decode)
        else:
            Rename(filename, options.decode)
    os.chdir("..")


if __name__ == "__main__":
    parser = ArgumentParser(description="Magic Rename")
    parser.add_argument("-D", "--decode",
                        action="store_true",
                        default=False,
                        help="if decode names, default encode names")
    parser.add_argument("filenames", nargs="*",
                        help="file names to rename")
    options = parser.parse_args()
    for filename in options.filenames:
        if os.path.isdir(filename):
            ErgodicDir(filename)
            Rename(filename, options.decode)
        else:
            Rename(filename, options.decode)
