#!/usr/bin/python

import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='list files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    parser.add_argument('--all', '-a', action='store_true', help='Include dotfiles in listing')
    return parser.parse_args()

def ls(args):
    
    dirs = os.listdir(args.directory)

    if args.all:
        dirs += [os.curdir, os.pardir]
    else:
        dirs = [dir for dir in dirs if dir[0] != '.']
    
    dirs.sort()

    for elem in dirs:
        print elem

if __name__ == '__main__':
    try:
        args = parse_args();
        ls(args)
    except OSError as err:
        print err