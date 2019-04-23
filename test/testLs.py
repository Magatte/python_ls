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

    def tearDown(self):
        print(self)

    def testLsDirectoryExist(self):
        capturedOutput = io.StringIO()                      # Create StringIO object
        sys.stdout = capturedOutput                         # and redirect stdout.
        self.options['all'] = False
        self.options['recursive'] = False
        self.options['onlyDir'] = False
        self.options['long'] = False
        self.options['reverse'] = False
        self.options['count'] = False
        with contextlib.redirect_stdout(capturedOutput):
            ls.ls(self.path, self.options)
        sys.stdout = sys.__stdout__                         # Reset redirect
        print ('Captured', capturedOutput.getvalue())       # Now works as before

if __name__ == '__main__':
    unittest.main()