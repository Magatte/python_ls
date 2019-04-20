#!/usr/bin/python

import os, sys, argparse
import shlex, struct, platform, subprocess


def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print "default"
        tuple_xy = (80, 25)      # default value
    return tuple_xy
 
 
def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass
 
 
def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


def pprint_list(input_list):
    (term_width, term_height) = get_terminal_size()
    if len( str(input_list) ) <= term_width:
        print('\t'.join(input_list))
        return

    repr_list = [repr(x) for x in input_list]
    repr_list = [i.replace("'", "") for i in repr_list]
    min_chars_between = 3 # a comma and two spaces
    usable_term_width = term_width - 3 # For '[ ' and ']' at beginning and end
    min_element_width = min( len(x) for x in repr_list ) + min_chars_between
    max_element_width = max( len(x) for x in repr_list ) + min_chars_between
    if max_element_width >= usable_term_width:
        ncol = 1
        col_widths = [1]
    else:
        # Start with max possible number of columns and reduce until it fits
        ncol = min( len(repr_list), usable_term_width / min_element_width  )
        while True:
            col_widths = [ max( len(x) + min_chars_between \
                                for j, x in enumerate( repr_list ) if j % ncol == i ) \
                                for i in range(ncol) ]
            if sum( col_widths ) <= usable_term_width: break
            else: ncol -= 1

    for i, x in enumerate(repr_list):
        if i != len(repr_list)-1:
            x += ' '
        sys.stdout.write( x.ljust( col_widths[ i % ncol ] ) )
        if i == len(repr_list) - 1:
            sys.stdout.write('\n')
        elif (i + 1) % ncol == 0:
            sys.stdout.write('\n')


def parse_args():
    parser = argparse.ArgumentParser(description='list files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    parser.add_argument('files', nargs='*')
    parser.add_argument('--all', '-a', action='store_true', help='Include dotfiles in listing')
    parser.add_argument('--long', '-l', action='store_true', help='Show size for each file or directory')
    parser.add_argument('--recursive', '-R', action='store_true', help='Recursively list subdirectories encountered')
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
        size = os.stat(os.path.join(path, elem)).st_size
        print "%d %s" % (size, elem)


def ls_recursive(path):
    for root, subdirs, files in os.walk(path):
        print('--\nroot = ' + root)
        
        merge_list = files + subdirs;
        merge_list.sort()
        pprint_list(merge_list)
        

def ls(args):
    dir_list = get_dir_list(args)
    path = os.path.abspath(args.directory)

    if args.recursive:
        ls_recursive(path)

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