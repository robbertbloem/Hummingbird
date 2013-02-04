from __future__ import print_function
from __future__ import division

import argparse
import unittest
import inspect

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.HBfunctions as HBFUN
import PythonTools.Debug as DEBUG

# init argument parser
parser = argparse.ArgumentParser(description='Command line arguments')

# add arguments
parser.add_argument("-v", "--verbose", action="store_true", help="Make PythonTools functions verbose")
parser.add_argument("-r", "--reload", action="store_true", help="Reload modules")
parser.add_argument("-s1", "--skip1", action="store_true", help="Skip testing suite 1")
parser.add_argument("-s2", "--skip2", action="store_true", help="Skip testing suite 2")
parser.add_argument("-s3", "--skip3", action="store_true", help="Skip testing suite 3")

# process
args = parser.parse_args()

# reload
if args.reload:
    reload(HBFUN)
    reload(DEBUG)


class Test_file_numbering(unittest.TestCase):

    def setUp(self):
        self.flag_verbose = args.verbose
        self.path = "/Users/robbert/Developer/Hummingbird/Tests/testdata/"
        self.filename = "file_numbering_1"
        self.extension = "txt"
        self.correct_result = "/Users/robbert/Developer/Hummingbird/Tests/testdata/file_numbering_1.txt"

    def test_file_numbering_1(self):
        """
        Test for file that does not exist.
        """
        result = HBFUN.file_numbering(self.path, self.filename, self.extension, flag_verbose = self.flag_verbose)
        self.assertEqual(result, self.correct_result)
    
    def test_file_numbering_2(self):
        """
        Test for file that does exist, it should now add _1 before the extension
        """
        filename = "file_numbering"
        result = HBFUN.file_numbering(self.path, filename, self.extension, flag_verbose = self.flag_verbose)
        self.assertEqual(result, self.correct_result)

    def test_file_numbering_3(self):
        """
        Test for file that does not exist, with a period after the filename
        """
        filename = "file_numbering_1."
        result = HBFUN.file_numbering(self.path, filename, self.extension, flag_verbose = self.flag_verbose)
        self.assertEqual(result, self.correct_result)

    def test_file_numbering_4(self):
        """
        Test for file that does not exist, with a period before the extension
        """
        extension = ".txt"
        result = HBFUN.file_numbering(self.path, self.filename, extension, flag_verbose = self.flag_verbose)
        self.assertEqual(result, self.correct_result)

    def test_file_numbering_5(self):
        """
        Test for file that does not exist, with path missing last /
        """
        path = "/Users/robbert/Developer/Hummingbird/Tests/testdata"
        result = HBFUN.file_numbering(path, self.filename, self.extension, flag_verbose = self.flag_verbose)
        self.assertEqual(result, self.correct_result)






class Test_make_jpg_html(unittest.TestCase):

    def setUp(self):
        self.flag_verbose = args.verbose

    def test_make_jpg_html_1(self):
        """
        Correct extension: jpeg
        """
        filename = "test.jpeg"
        result = HBFUN.make_jpg_html(filename)
        self.assertEqual(result, "test.html")


    def test_make_jpg_html_2(self):
        """
        Correct extension: jpg
        """
        filename = "test.jpg"
        result = HBFUN.make_jpg_html(filename)
        self.assertEqual(result, "test.html")

    def test_make_jpg_html_3(self):
        """
        Incorrect extension: abc
        """
        filename = "test.abc"
        DEBUG.verbose("Error is intentional", True)
        result = HBFUN.make_jpg_html(filename)
        self.assertFalse(result)



# class Test_check_path_exists(unittest.TestCase):
# 
#     def setUp(self):
#         self.flag_verbose = args.verbose
#         self.prompt = "Test user input: "   
#     
#     def test_ask_user_1(self):
#         
#         result = HBFUN.ask_user_confirmation(self.prompt)
# 
#         print(result)




  
if __name__ == '__main__': 



    if args.skip1 == False:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_file_numbering)
        unittest.TextTestRunner(verbosity=1).run(suite)    
    else:
        DEBUG.verbose("Skipping suite 1: file numbering", True)

    if args.skip2 == False:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_make_jpg_html)
        unittest.TextTestRunner(verbosity=1).run(suite)    
    else:
        DEBUG.verbose("Skipping suite 2: make jpg html", True)
    
    # if args.skip3 == False:
    #     suite = unittest.TestLoader().loadTestsFromTestCase(Test_check_path_exists)
    #     unittest.TextTestRunner(verbosity=1).run(suite)    
    # else:
    #     DEBUG.verbose("Skipping suite 3: check if path exists", True)        