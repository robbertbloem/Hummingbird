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

import PythonTools.Debug as DEBUG

def file_numbering(path, filename, extension, silence = True):
    """
    file_numbering: produces a unique filename
    
    20130103: started the function
    
    INPUT:
    - path (str): path
    - filename (str): filename
    - extension (str): extension
    Note that filename should not end with a period, while the extenstion should not start with one.
    
    OUTPUT:
    - a unique path_and_filename
    
    """
    
    if filename[-1] == ".":
        filename = filename[:-1]
    if extension[0] == ".":
        extension = extension[1:]


    if os.access(path + filename + "." + extension, os.F_OK):
        i = 1
        while os.access(path + filename + "_" + str(i) + "." + extension, os.F_OK):
            i += 1
        
        if silence == False:
            DEBUG.printWarning("WARNING: props filename is numbered", inspect.stack())
        return path + filename + "_" + str(i) + "." + extension
    else:
        return path + filename + "." + extension




def get_exif(filename):
    """
    get_exif: read the exif data
    
    20130103: copied the function... from StackOverflow?
    
    INPUT:
    - filename (str)
    
    OUTPUT:
    - dictionary with exif data
    
    """
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
    """
    make_jpg_html: converts 'photo.jpg' to 'photo.html'
    
    20130102: started the function
    
    """
    
    if name[-4:] == "jpeg":
        return name[:-4] + "html"
    elif name[-3:] == "jpg":
        return name[:-3] + "html"
    else: 
        DEBUG.printError("Extension is not 'jpg' or 'jpeg'", inspect.stack())
        return False





def resize_pics(source_path, 
    dest_path,
    source_to_pics_list, 
    max_pic_size,
    flag_verbose = False):
    
    """
    resize_pics: read photo from source, copy and resize it to destination
    
    20130103: started the function

    INPUT:
    - source_path (str): complete path of the original photos
    - dest_path (str): complete path of the destination of the photos
    - source_to_pics_list (list): array with a list of filenames
    - max_pic_size (int): maximum size of the photos
        - it will use the long edge
        - photos that are smaller will not be resized.
    
    REMARK:
    The exif data is copied from the source to destination file (strictly speaking, this means the exif data of the size is incorrect). This is done independently from reading the exif-data that is used in the photo-object.
    
    """
    
    DEBUG.verbose("HBfunctions.resize_pics(): from " + source_path + " to " + dest_path, True)

    
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

        DEBUG.verbose("resize: " + FILE + ", from: " + str(w) + "x" + str(h) + " to " + str(new_width) + "x" + str(new_height) + " (WxH)", flag_verbose)
        
        # save the result
        img.save(dest_file)

        # copy the exif data
        os.system("exiftool -tagsFromFile " + source_file + " " + dest_file + " -overwrite_original")

    return True



def make_thumbs(source_path, 
    dest_path, 
    source_to_thumbs_list, 
    thumb_size,
    flag_verbose = False): 
    
    """
    make_thumbs: crop, resize and copy photos to use as thumbnails.
    
    20130103: started the function
    
    For details on input, see 'resize_pics'. This function will first determine the short edge. It will then create a box of size short_edge x short_edge, centered in the long_edge. This is cropped and then resized to thumb_size.
    
    """
    
    DEBUG.verbose("HBfunctions.resize_thumbs(): from " + source_path + " to " + dest_path, True)    
    
    for FILE in source_to_thumbs_list:
        
        source_file = source_path + FILE
        dest_file = dest_path + FILE
    
        img = Image.open(source_file)
    
        # determine current size of photo
        w, h = img.size
    
        DEBUG.verbose("thumbs: " + FILE + ", width: " + str(w) + ", height: " + str(h), flag_verbose)
    
        if w > h: # landscape
            box = (int(w/2 - h/2), 0, int(w/2 + h/2), h)
        else:
            box = (0, int(h/2 - w/2), w, int(w/2 + h/2))            
        
        # crop and resize  
        img = img.crop(box).resize((thumb_size, thumb_size), Image.ANTIALIAS)
    
        img.save(dest_file)

        # copy exif data
        os.system("exiftool -tagsFromFile " + source_file + " " + dest_file + " -overwrite_original")
     
    return True








def ask_user_confirmation(prompt):
    """
    ask_user_confirmation: for a prompt, ask for yes or no reply
    
    20130103: started the function
    
    INPUT:
    - prompt (str): question, like 'This will destroy the universe. y/n?'
    
    INTERACTION:
    - The user should answer with Y, y, yes, N, n or no. Otherwise the prompt will be shown again. 
    
    OUTPUT:
    If the answer is yes, it will return True, otherwise False.
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
    check_path_exists: does 'path' exist? 
    
    20130103: started the function

    INPUT:
    - path (str): a path. The path can be a foldername or a filename.
    
    OUTPUT:
    - True if the path exists, False if it doesn't
 
    """
    
    DEBUG.verbose("\nHBfunctions/check_folder_exists(): " + path, flag_verbose)

    res = os.access(path, os.F_OK)
    
    if flag_verbose:
        if res:
            DEBUG.verbose("  folder exists", flag_verbose)
        else:
            DEBUG.verbose("  folder does not exist", flag_verbose)
        
    return res

    


def check_and_make_folder(path, flag_verbose = False):
    """
    check_and_make_folder: check if a folder exists, if not, create it
    
    20130103: started the function
    
    INPUT:
    - path (str)
    
    """
    
    verbose("\nHBfunctions/check_and_make_folder(): " + path, flag_verbose)
    
    if os.access(path, os.F_OK) == False:
        os.mkdir(path)
        DEBUG.verbose("  created folder", flag_verbose)
    elif flag_verbose:
        DEBUG.verbose("  folder existed", flag_verbose)




def check_path(path, flag_verbose = False):
    """
    check_path: Convention is that a foldername always ends in a slash and never begins with one. This function checks if a foldername or path ends in a slash. Exception is when the path is root, then it does start with a slash.
    
    20130103: started the function
    
    """
    DEBUG.verbose("\nHBfunctions/check_path(): " + path, flag_verbose)
    # check at beginning
    if path[:5] == "Users":
        path = "/" + path
    elif path[0] == "/" and path[:6] != "/Users":
        path = path[1:]
    # check the end
    if path[-1] != "/":
        path = path + "/"
    DEBUG.verbose("  check_path> " + path, flag_verbose)
    return path
        
 




 
if __name__ == "__main__":
    pass
    

    