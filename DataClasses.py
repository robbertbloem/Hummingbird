"""
dataclasses.py

DESCRIPTION
    This file contains all the high-level stuff for classes


CHANGELOG
    RB 20091214 - first draft.
    RB 20110908 - combined some stuff together
    RB 20130102 - copied from croc

"""

from __future__ import print_function
from __future__ import division

import numpy
import pylab

import time
import os.path
import shelve
import sys


class ClassTools(object):
    """
    A way to print the whole class in one go.
    It prints the key and the value.
    """
    def gatherAttrs(self):
        attrs=[]
        for key in sorted(self.__dict__):
            attrs.append("\t%20s  =  %s\n" % (format_key(key), format_print(getattr(self, key))))
        return " ".join(attrs)

    def __str__(self):
        return "[%s:\n %s]" % (self.__class__.__name__, self.gatherAttrs())








        
        
        
        











####################
# SHELVE FUNCTIONS #
####################

def make_db(array_of_class_instances, path_and_filename, use_shelve = False, flag_debug = False, flag_overwrite = False):
    """
    Makes a database and writes all values.
    The input should be an array with class instances, not a class instance itself! If the database already exists, it will update the values. Make sure that everything stored in the database has the same class.

    CHANGELOG:
    20120302 RB: tried to implement the cPickle instead of shelve (which uses pickle, which should be slower than cPickle). However, there was no notable increase in speed and it was abandoned, because it would cause confusion.

    """

    if path_and_filename[-7:] != ".pickle":
        path_and_filename += ".pickle"

    if flag_overwrite:
        print("make_db: overwrite flag is True")
        flag = "n"
    else:
        flag = "c"

    print("\n" + path_and_filename)    

    if flag_debug:
        print("Saving using shelve")

    db = shelve.open(path_and_filename, flag = flag)

    for object in array_of_class_instances:
        db[object.album_title] = object

    db.close()

    os.system("chmod 777 " + path_and_filename)



def import_db(path_and_filename, print_keys = False):
    """
    Imports a database. 
    The function checks for the existence of the database. It returns "False" 
        if the file doesn't exist. Otherwise, it will return an array with
        class instances.
    """

    if path_and_filename[-7:] != ".pickle":
        path_and_filename += ".pickle"


    if os.path.isfile(path_and_filename) == True:

        db=shelve.open(path_and_filename)

        array_of_class_instances = []

        for key in db:
            if print_keys:
                print(key)
            array_of_class_instances.append(db[key])

        db.close()

        return array_of_class_instances


    else:
        print("classtools.import_db: The file doesn't exist!")
        return False


####################
# HELPER FUNCTIONS #
####################

def format_print(var):
    """
    format_print is a helper function for the gatherAttrs function. 
    There are a few situations:
        1) var is not a list or an ndarray, it will print the value. This include tuples
        2) var is an ndarray, the shape will be printed
        3) var is a time. It will return a readable string with the time.
        3) the var is a list, it will do recursion to print either 1 or 2
    Examples:
        42          => 42
        "car"       => "car"
        [1,2]       => [1,2]
        ndarray     => shape
        [1,ndarray] => [1, shape]
    """
    # list
    if type(var) == list:
        typ = range(len(var))       
        for i in range(0, len(var)):
            typ[i] = (format_print(var[i]))
        return typ
    # ndarray
    elif type(var) == numpy.ndarray:
        a = numpy.shape(var)
        if len(a) == 1: 
            return str(a[0]) + " x 1"
        elif len(a) == 2:
            return str(a[0]) + " x " + str(a[1])
        elif len(a) == 3:
            return str(a[0]) + " x " + str(a[1]) + " x " + str(a[2])

        else: 
            return str(a[0]) + " x " + str(a[1]) + " x " + str(a[2]) + " x ..."
    # time
    elif type(var) == time.struct_time: 
        var = time.strftime("%a, %d %b %Y %H:%M:%S", var)
        return var
    # elif type(var) == int:
        # return var
    elif type(var) == float:
        return round(var, 2)
    elif type(var) == numpy.float64:
        return round(var, 2)
    # the rest
    else:
        return var

def format_key(key):
    """
    Strips keys from _. These keys are semi-protected and should be run through the getter and setter methods.
    """
    if key[0] == "_":
        key = key[1:]
    else:
        pass

    return key