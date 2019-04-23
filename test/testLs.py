import unittest
import contextlib
import io
import sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from src import ls

class testFunctionLs(unittest.TestCase):
    
    def setUp(self):
        self.path = 'test/Durex'
        self.options = dict()

    def testLsDirectoryExist(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = False
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = ['Dockerfile', 'Durex', 'Durex.service', 'Makefile', 'README.md', 'clean.sh', 'clients', 'daemon', 'includes', 'obj', 'reset.sh', 'show_log.sh', 'src']
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsDirectoryNotExist(self):
        self.path = 'test/toto'
        self.options['all'] = False
        self.options['recursive'] = False
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        with self.assertRaises(OSError):
            ls.ls(self.path, self.options)

    def testLsAll(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = True
        self.options['recursive'] = False
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = ['.', '..', '.ignore', '.zombie', 'Dockerfile', 'Durex', 'Durex.service', 'Makefile', 'README.md', 'clean.sh', 'clients', 'daemon', 'includes', 'obj', 'reset.sh', 'show_log.sh', 'src']
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsOnlyDir(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = False
        self.options['onlyDir'] = True
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = ['.', '..', '.zombie', 'clients', 'daemon', 'includes', 'obj', 'src', '9', 'files']
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsLong(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = False
        self.options['onlyDir'] = False
        self.options['long'] = True
        self.options['reverse'] = False
        self.options['count'] = False
        expectedOutput = ['463', 'Dockerfile', '28592', 'Durex', '227', 'Durex.service', '3863', 'Makefile', '6856', 'README.md', '243', 'clean.sh', '4096', 'clients', '4096', 'daemon', '4096', 'includes', '4096', 'obj', '39', 'reset.sh', '84', 'show_log.sh', '4096', 'src']
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())

    def testLsReverse(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = False
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = True
        self.options['count'] = False
        expectedOutput = ['Dockerfile', 'Durex', 'Durex.service', 'Makefile', 'README.md', 'clean.sh', 'clients', 'daemon', 'includes', 'obj', 'reset.sh', 'show_log.sh', 'src']
        expectedOutput.reverse()
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
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
        expectedOutput = ['.', '..', '.zombie', 'clients', 'daemon', 'includes', 'obj', 'src', '9', 'files']
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        self.assertEqual(len(expectedOutput), len(capturedOutput.getvalue().split()))
        self.assertEqual(expectedOutput, capturedOutput.getvalue().split())


if __name__ == '__main__':
    unittest.main()