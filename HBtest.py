from __future__ import print_function
from __future__ import division

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.HBfunctions as HBFun


def test_check_path():
    print("HBtest/test_check_path()")
    
    verbose = True
    
    path = "fiets"
    out = HBFun.check_path(path, verbose)
    if out == "fiets/":
        print("  pass")
    else:
        print("  FAIL:", out)

    path = "/fiets"
    out = HBFun.check_path(path, verbose)
    if out == "fiets/":
        print("  pass")
    else:
        print("  FAIL:", out) 

    path = "/Users/fiets"
    out = HBFun.check_path(path, verbose)
    if out == "/Users/fiets/":
        print("  pass")
    else:
        print("  FAIL:", out)

    path = "Users/fiets"
    out = HBFun.check_path(path, verbose)
    if out == "/Users/fiets/":
        print("  pass")
    else:
        print("  FAIL:", out) 


def test_check_path_exists():
    
    print("HBtest/test_check_path_exists()")
    
    verbose = True
    
    path = "/Users/robbert/"  
    res = HBFun.check_path_exists(path, verbose)
    if res == True:
        print("  pass")
    else:
        print("  FAIL:", res)
    
    path = "/Users/bernard/"  
    res = HBFun.check_path_exists(path, verbose)
    if res == False:
        print("  pass")
    else:
        print("  FAIL:", res)
    
    path = "/Users/robbert/croc_tests.py"  
    res = HBFun.check_path_exists(path, verbose)
    if res == True:
        print("  pass")
    else:
        print("  FAIL:", res)

    path = "/Users/robbert/does_not_exist.py"  
    res = HBFun.check_path_exists(path, verbose)
    if res == False:
        print("  pass")
    else:
        print("  FAIL:", res)  

def test_ask_user_confirmation():
    
    answer = HBFun.ask_user_confirmation("This will destroy the world y/n: ")
    print(answer)

if __name__ == "__main__": 
    test_check_path()
    test_check_path_exists()
    # test_ask_user_confirmation()