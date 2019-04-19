#!/usr/bin/python

import os
import argparse

def ls():
    parser = argparse.ArgumentParser(description='list files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    args = parser.parse_args()
    for elem in os.listdir(args.directory):
        print elem

if __name__ == '__main__':
    ls()