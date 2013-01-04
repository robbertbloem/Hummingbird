from __future__ import print_function
from __future__ import division

import os
import inspect

import Image
import PIL
import PIL.Image
import PIL.ExifTags

import numpy
import matplotlib 
import matplotlib.pyplot as plt

def file_numbering(path, filename, extension):

    if os.access(path + filename + "." + extension, os.F_OK):
        i = 1
        while os.access(path + filename + "_" + str(i) + "." + extension, os.F_OK):
            i += 1

        printWarning("WARNING: props filename is numbered", inspect.stack())
        return path + filename + "_" + str(i) + "." + extension
    else:
        return path + filename + "." + extension




def get_exif(filename):
    ret = {}
    img = PIL.Image.open(filename)
    info = img._getexif()
    for tag, value in info.items():
        decoded = PIL.ExifTags.TAGS.get(tag, tag)
        if decoded == 42036:
            decoded = "Lens"
        ret[decoded] = value
    return ret  




def make_jpg_html(name):
    return name[:-3] + "html"





def resize_pics(source_path, 
    dest_path,
    source_to_pics_list, 
    max_pic_size,
    flag_verbose = False):
    
    for FILE in source_to_pics_list:
        
        source_file = source_path + FILE
        dest_file = dest_path + FILE
        
        # import file
        img = Image.open(source_file)
        
        # determine current size of photo
        w, h = img.size
        
        # make smaller photo to max_pic_size. if photo is already smaller, don't do anything
        if w >= h and w > max_pic_size: # landscape
            new_width = max_pic_size
            new_height = int(h/(w/max_pic_size))
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        elif w < h and h > max_pic_size: # portrait
            new_height = max_pic_size
            new_width = int(w/(h/max_pic_size))
            img = img.resize((new_width, new_height), Image.ANTIALIAS)   

        verbose("resize: " + FILE + ", from: " + str(w) + "x" + str(h) + " to " + str(new_width) + "x" + str(new_height) + " (WxH)", flag_verbose)
        
        # save the result
        img.save(dest_file)

        os.system("exiftool -tagsFromFile " + source_file + " " + dest_file + " -overwrite_original")

    return True



def make_thumbs(source_path, 
    dest_path, 
    source_to_thumbs_list, 
    thumb_size,
    flag_verbose = False): 
      
    for FILE in source_to_thumbs_list:
        
        source_file = source_path + FILE
        dest_file = dest_path + FILE
    
        img = Image.open(source_file)
    
        # determine current size of photo
        w, h = img.size
    
        verbose("thumbs: " + FILE + ", width: " + str(w) + ", height: " + str(h), flag_verbose)
    
        if w > h: # landscape
            box = (int(w/2 - h/2), 0, int(w/2 + h/2), h)
        else:
            box = (0, int(h/2 - w/2), w, int(w/2 + h/2))            
            
        img = img.crop(box).resize((thumb_size, thumb_size), Image.ANTIALIAS)
    
        img.save(dest_file)

        os.system("exiftool -tagsFromFile " + source_file + " " + dest_file + " -overwrite_original")
     
    return True








def ask_user_confirmation(prompt):
    """
    Ask the user a prompt, which can be answered with Y, y, yes, N, n or no. Otherwise the prompt will be shown again. If the answer is yes, it will return True, otherwise False.
    """
    
    while True:
        reply = raw_input(prompt + " ")
        
        if reply == "Y" or reply == "y" or reply == "yes":
            reply = True
            break
        elif reply == "N" or reply == "n" or reply == "no":
            reply = False
            break
        else:
            print("Try again...")
        
    return reply
        
        




def check_path_exists(path, flag_verbose = False):
    """
    Check if a folder or file exists, Returns True or False
    """
    verbose("\nHBfunctions/check_folder_exists(): " + path, flag_verbose)

    res = os.access(path, os.F_OK)
    
    if verbose:
        if res:
            print("  folder exists")
        else:
            print("  folder does not exist")
        
    return res

    


def check_and_make_folder(path, flag_verbose = False):
    
    verbose("\nHBfunctions/check_and_make_folder(): " + path, flag_verbose)
    
    if os.access(path, os.F_OK) == False:
        os.mkdir(path)
        verbose("  created folder", flag_verbose)
    elif flag_verbose:
        verbose("  folder existed", flag_verbose)




def check_path(path, flag_verbose = False):
    """
    Convention is that a foldername always ends in a slash and never begins with one. This function checks if a foldername or path ends in a slash. Exception is when the path is root, then it does start with a slash.
    """
    verbose("\nHBfunctions/check_path(): " + path, flag_verbose)
    # check at beginning
    if path[:5] == "Users":
        path = "/" + path
    elif path[0] == "/" and path[:6] != "/Users":
        path = path[1:]
    # check the end
    if path[-1] != "/":
        path = path + "/"
    verbose("  check_path> " + path, flag_verbose)
    return path
        
 
def printError(string, location = []):
    if location == []:
        print("\033[1;31mERROR: " + string + "\033[1;m")
    else:
        print("\033[1;31mERROR (" + location[0][1] + ":" + location[0][3] + "): " + string + "\033[1;m")


def printWarning(string, location = []):
    if location == []:
        print("\033[1;35mWARNING: " + string + "\033[1;m")
    else:
        print("\033[1;35mWARNING (" + location[0][1] + "): " + string + "\033[1;m")

def verbose(string, flag_verbose):
    if flag_verbose:
        print("\033[1;34m" + string + "\033[1;m")









 
if __name__ == "__main__":
    pass
    

    