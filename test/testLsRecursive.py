import unittest
import contextlib
import io
import sys, os
import difflib
# sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from src import ls

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class testFunctionLs(unittest.TestCase):
    
    def setUp(self):
        self.path = 'test/Durex/obj'
        self.options = dict()

    def testLsRecursiveDirectoryExist(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = True
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = [bcolors.OKBLUE + '--', self.path + bcolors.ENDC, 'rel', bcolors.OKBLUE + '--', self.path + '/rel' + bcolors.ENDC, 'src', bcolors.OKBLUE + '--', self.path + '/rel/src' + bcolors.ENDC, 'install.d', 'install.o', 'main.d', 'main.o']
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsRecursiveDirectoryDefault(self):
        self.path = '.'
        capturedOutput = io.StringIO()                      # Create StringIO object
        self.options['all'] = False
        self.options['recursive'] = True
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        file = open('test/recursiveDefault.txt', 'r')
        expectedOutput = file.read()
        file.close()
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        for line in difflib.unified_diff(expectedOutput, capturedOutput.getvalue()):
            self.assertEqual(line, "")

    def testLsRecursiveDirectoryNotExist(self):
        self.path = 'test/toto'
        self.options['all'] = False
        self.options['recursive'] = True
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        with self.assertRaises(OSError):
            ls.lsRecursive(self.path, self.options)

    def testLsRecursiveAll(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = True
        self.options['recursive'] = True
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = [bcolors.OKBLUE + '--', self.path + bcolors.ENDC, '.', '..', 'rel', bcolors.OKBLUE + '--', self.path + '/rel' + bcolors.ENDC, '.', '..', 'src', bcolors.OKBLUE + '--', self.path + '/rel/src' + bcolors.ENDC, '.', '..', 'install.d', 'install.o', 'main.d', 'main.o']
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsRecursiveOnlyDir(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = True
        self.options['onlyDir'] = True
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = [bcolors.OKBLUE + '--', self.path + bcolors.ENDC, '.', '..', 'rel', '0', 'file', bcolors.OKBLUE + '--', self.path + '/rel' + bcolors.ENDC, '.', '..', 'src', '0', 'file', bcolors.OKBLUE + '--', self.path + '/rel/src' + bcolors.ENDC, '.', '..', '4', 'files']
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsRecursiveLong(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = True
        self.options['onlyDir'] = False
        self.options['long'] = True
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = [bcolors.OKBLUE + '--', self.path + bcolors.ENDC, '4096', 'rel', bcolors.OKBLUE + '--', self.path + '/rel' + bcolors.ENDC, '4096', 'src', bcolors.OKBLUE + '--', self.path + '/rel/src' + bcolors.ENDC, '194', 'install.d', '1816', 'install.o', '188', 'main.d', '3040', 'main.o']
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsRecursiveReverse(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = True
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = True
        self.options['count'] = False
        expectedOutput = [bcolors.OKBLUE + '--', self.path + bcolors.ENDC, 'rel', bcolors.OKBLUE + '--', self.path + '/rel' + bcolors.ENDC, 'src', bcolors.OKBLUE + '--', self.path + '/rel/src' + bcolors.ENDC, 'main.o', 'main.d', 'install.o', 'install.d']
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsAllOnlyDir(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = True
        self.options['recursive'] = False
        self.options['onlyDir'] = True
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = [bcolors.OKBLUE + '--', self.path + bcolors.ENDC, '.', '..', 'rel', '0', 'file', bcolors.OKBLUE + '--', self.path + '/rel' + bcolors.ENDC, '.', '..', 'src', '0', 'file', bcolors.OKBLUE + '--', self.path + '/rel/src' + bcolors.ENDC, '.', '..', '4', 'files']
        with contextlib.redirect_stdout(capturedOutput):
            ls.lsRecursive(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())


if __name__ == '__main__':
    unittest.main()