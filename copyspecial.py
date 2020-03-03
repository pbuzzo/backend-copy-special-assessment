#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import re
import os
import shutil
import subprocess
import argparse
import zipfile
import commands
import sys

# This is to help coaches and graders identify student assignments
__author__ = "Patrick Buzzo"

special_path_list = []
rel_path_list = []


def get_special_paths(dir):
    if dir == '.':
        for i in os.listdir('./'):
            if re.search(r'__\w+__', i):
                special_path_list.append(os.path.abspath(i))
        for k in special_path_list:
            rel_path_list.append(dir[1:] + '/' + os.path.relpath(k))
    elif dir != '.':
        for i in os.listdir(dir):
            if re.search(r'__\w+__', i):
                special_path_list.append(os.path.abspath(i))
        for k in special_path_list:
            rel_path_list.append(dir[1:] + '/' + os.path.relpath(k))


def copy_to(paths, dir):
    if dir == '.':
        for i in rel_path_list:
            with open(i[1:], 'r') as f:
                shutil.copyfile(i[1:], 'copy ' + i[1:])
                # lines = f.readlines()
                # with open('copy ' + i[1:], "w") as f1:
                #     for i in lines:
                #         f1.write(i)
    elif dir != '.':
        for i in rel_path_list:
            with open(i[1:], 'r') as f:
                shutil.copyfile(i[1:], dir + 'copy ' + i[1:])
                # lines = f.readlines()
                # with open(dir + 'copy ' + i[1:], "w") as f1:
                #     for i in lines:
                #         f1.write(i)


def zip_to(paths, zippath):
    cmd = 'zip -j ' + zippath + ' '
    # for item in paths[:-1]:
    cmd += paths[0] + ' ' + paths[1]
    print("Command I'm going to do: " + cmd)
    (k, i) = commands.getstatusoutput(cmd)
    if k:
        sys.stderr.write(k)
        sys.exit(1)
    # https://stackoverflow.com/questions/31420317/
    # how-to-understand-sys-stdout-and-sys-stderr-in-python


def main():
    # This snippet will help you get started with the argparse module.
    # TODO need an argument to pick up 'from_dir'
    parser = argparse.ArgumentParser()
    parser.add_argument('files', help='files to find absolute path for')
    parser.add_argument('--todir', dest='direct', type=str,
                        nargs='+', help='dest dir for special files')
    parser.add_argument('--tozip', dest='zip', type=str,
                        nargs='+', help='dest zipfile for special files')
    args = parser.parse_args()
    direct = args.direct
    z = args.zip

    if direct:
        get_special_paths(direct[0])
        copy_to(special_path_list, direct[0])
    elif z:
        get_special_paths(z[1])
        zip_to(special_path_list, z[0])
    else:
        get_special_paths(sys.argv[1])
        for i in special_path_list:
            print(i + '\n')


if __name__ == "__main__":
    main()


# get_special_paths('.')   # TEST
# copy_to(special_path_list, '.')   # TEST
# zip_to(special_path_list, 'patholis.zip')  # TEST
