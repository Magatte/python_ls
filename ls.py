#!/usr/bin/python

import os, sys, argparse
import struct, platform
from Carbon.Files import newLineBit
from matplotlib import path

 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getTerminalSizeLinux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
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


def getTerminalSize():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    currentOs = platform.system()
    tupleXY = None
    
    if currentOs in ['Linux', 'Darwin'] or currentOs.startswith('CYGWIN'):
        tupleXY = getTerminalSizeLinux()
    if tupleXY is None:
        print "default"
        tupleXY = (80, 25)      # default value
    return tupleXY
 
 
def pprintList(inputList):
    (termWidth, termHeight) = getTerminalSize()
    termHeight = termHeight
    if len( str(inputList) ) <= termWidth:
        print('\t'.join(inputList))
        return

    reprList = [repr(x) for x in inputList]
    reprList = [i.replace("'", "") for i in reprList]
    minCharsBetween = 3 # two spaces
    usableTermWidth = termWidth - 3
    minElementWidth = min( len(x) for x in reprList ) + minCharsBetween
    maxElementWidth = max( len(x) for x in reprList ) + minCharsBetween
    if maxElementWidth >= usableTermWidth:
        ncol = 1
        colWidths = [1]
    else:
        # Start with max possible number of columns and reduce until it fits
        ncol = min( len(reprList), usableTermWidth / minElementWidth  )
        while True:
            colWidths = [ max( len(x) + minCharsBetween \
                                for j, x in enumerate( reprList ) if j % ncol == i ) \
                                for i in range(ncol) ]
            if sum( colWidths ) <= usableTermWidth: break
            else: ncol -= 1

    for i, x in enumerate(reprList):
        if i != len(reprList) - 1:
            x += ' '
        sys.stdout.write( x.ljust( colWidths[ i % ncol ] ) )
        if i == len(reprList) - 1:
            sys.stdout.write('\n')
        elif (i + 1) % ncol == 0:
            sys.stdout.write('\n')


def parse_args():
    parser = argparse.ArgumentParser(description='list files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    parser.add_argument('--all', '-a', action='store_true', help='Include dotfiles in listing')
    parser.add_argument('--recursive', '-R', action='store_true', help='Recursively list subdirectories encountered')
    parser.add_argument('--onlyDir', '-d', action='store_true', help='Only show directories and the number of files of each directory')
    parser.add_argument('--long', '-l', action='store_true', help='Show size for each file or directory')
    parser.add_argument('--reverse', '-r', action='store_true', help='Reverse the display order')
    parser.add_argument('--count', '-c', action='store_true', help='Show the number of lines of each file in a directory')
    return parser.parse_args()


def ls_long(dir_list, path):
    for elem in dir_list:
        size = os.stat(os.path.join(path, elem)).st_size
        print "%d %s" % (size, elem)


def display(dirList, path, options):
    if options['reverse']:
        dirList.reverse()
    if options['long']:
        dirList = [ str(os.stat(os.path.join(path, elem)).st_size) + ' ' + elem for elem in dirList ]
    # if options['count']:
    #     # modify list to put count
    pprintList(dirList)


def lsRecursive(path, options):
    for root, subdirs, files in os.walk(path):
        if options['all']:
            newList = files + subdirs
            newList += [os.curdir, os.pardir]
        elif options['onlyDir']:
            options['all'] = False;
            newList = subdirs
        else:
            subdirs[:] = [ elem for elem in subdirs if elem[0] != '.' ]
            files = [ elem for elem in files if elem[0] != '.' ]
            newList = files + subdirs
        print(bcolors.OKBLUE + '--\n' + root + bcolors.ENDC)
        newList.sort()
        display(newList, root, options)
        if (options['onlyDir']):
            nbOfFiles = len(files)
            word = 'file'
            if nbOfFiles > 1:
                word = word.replace('file', 'files')
            print "%d %s" % (nbOfFiles, word)



def ls(path, options):
    dirList = os.listdir(path)

    if options['onlyDir']:
        options['all'] = False;
        dirList += [os.curdir, os.pardir]
        dirList = [ elem for elem in dirList if os.path.isdir(os.path.join(path, elem)) ]
    elif options['all']:
        dirList += [os.curdir, os.pardir]
    else:
        dirList = [ elem for elem in dirList if elem[0] != '.' ]
    dirList.sort()
    display(dirList, path, options);
    if (options['onlyDir']):
            nbOfFiles = len([ elem for elem in os.listdir(path) if os.path.isfile(os.path.join(path, elem))])
            word = 'file'
            if nbOfFiles > 1:
                word = word.replace('file', 'files')
            print "%d %s" % (nbOfFiles, word)


def search(path, options):
    if options['recursive']:
        return lsRecursive(path, options)
    else:
        return ls(path, options)


if __name__ == '__main__':
    try:
        args = parse_args();
        path = os.path.abspath(args.directory)
        options = dict()

        options['all'] = args.all
        options['recursive'] = args.recursive
        options['onlyDir'] = args.onlyDir
        options['long'] = args.long
        options['reverse'] = args.reverse
        options['count'] = args.count

        search(path, options)
    except OSError as err:
        print err