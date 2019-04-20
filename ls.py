#!/usr/bin/python

import os, argparse

def parse_args():
    parser = argparse.ArgumentParser(description='list files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    parser.add_argument('files', nargs='*')
    parser.add_argument('--all', '-a', action='store_true', help='Include dotfiles in listing')
    parser.add_argument('--long', '-l', action='store_true', help='Show detailed listing')
    return parser.parse_args()

def get_dir_list(args):
    dir_list = os.listdir(args.directory)

    if args.all:
        dir_list += [os.curdir, os.pardir]
    else:
        dir_list = [elem for elem in dir_list if elem[0] != '.']

    dir_list.sort()
    
    return dir_list

def ls_long(dir_list, path):
    for elem in dir_list:
        size = os.stat(path + '/' + elem).st_size
        print "%d %s" % (size, elem)

def ls(args):
    dir_list = get_dir_list(args)
    path = args.directory

    if args.long:
        ls_long(dir_list, path)
    else:
        for elem in dir_list:
            print elem

if __name__ == '__main__':
    try:
        args = parse_args();
        ls(args)
    except OSError as err:
        print err