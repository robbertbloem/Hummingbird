from __future__ import print_function
from __future__ import division

import os
import csv

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.DataClasses as DC
import Hummingbird.HBfunctions as HBFUN
import Hummingbird.HBphoto as HBPh

class event(DC.ClassTools):

    def __init__(self, event_title, event_dir, event_dir_src, album_title, album_path, source_path, pics_dir, thumbs_dir, resources_dir, html_dir, verbose):

        HBFUN.verbose("HBevent/__init__: " + event_title + ", " + event_dir + ", " + album_title + " etc.", verbose)

        # "inherited"
        self.album_title = album_title
        self.album_path = album_path      
        self.source_path = source_path
        self.pics_dir = pics_dir       
        self.thumbs_dir = thumbs_dir  
        self.resources_dir = resources_dir
        self.html_dir = html_dir

        # own   
        self.event_title = event_title
        self.event_dir = event_dir      # correctness already checked by album
        self.event_dir_src = event_dir_src  # source of the pics

        self.disabled = False           # disable but not delete event
        
        self.photo_array = []           # array with photos
        
        self.event_thumb = 0            # index of thumb for event
  
        self.max_pic_size = 1500        # max size for pictures
        self.thumb_size = 150           # size for thumbs
        
        self.make_folders(verbose)


    def make_folders(self, verbose = False):
        """
        Create the web-folders
        """
        HBFUN.verbose("\nHBevent/make_folders()", verbose)
        
        path = self.album_path + self.pics_dir + self.event_dir
        HBFUN.check_and_make_folder(path, verbose)
        
        path = self.album_path + self.thumbs_dir + self.event_dir
        HBFUN.check_and_make_folder(path, verbose)
        
        path = self.album_path + self.resources_dir + self.event_dir
        HBFUN.check_and_make_folder(path, verbose)
                
        path = self.album_path + self.html_dir + self.event_dir
        HBFUN.check_and_make_folder(path, verbose)  
        
        return True         



        
    def add_and_resize_photos(self, flag_redo_resize = False, verbose = False):
        
        HBFUN.verbose("\nHBevent/add_and_resize_photos(): redo resize? " + str(flag_redo_resize), verbose)
        
        # compare the contents of the folders. No need to do double work!
        source_list = os.listdir(self.source_path + self.event_dir_src)
        pics_list = os.listdir(self.album_path + self.pics_dir + self.event_dir)
        
        # clean up the source list from non-jpgs
        source_list = [n for n in source_list if n[-4:] == ".jpg"]
        
        # remove items that already have been resized
        if flag_redo_resize:
            source_to_pics_list = source_list
        else:
            source_to_pics_list = [n for n in source_list if n not in pics_list]
            HBFUN.verbose(str(len(source_to_pics_list)) + " of " + str(len(source_list)) + " pics will be resized", verbose)

        src_path = self.source_path + self.event_dir_src
        dest_path = self.album_path + self.pics_dir + self.event_dir

        HBFUN.resize_pics(src_path, dest_path, source_to_pics_list, self.max_pic_size, verbose)


    def add_and_resize_thumbs(self, flag_redo_thumbs = False, verbose = False):
        
        HBFUN.verbose("\nHBevent/add_and_resize_thumbs(): redo resize? " + str(flag_redo_thumbs), verbose)
        
        # compare the contents of the folders. No need to do double work!
        source_list = os.listdir(self.source_path + self.event_dir_src)
        thumbs_list = os.listdir(self.album_path + self.thumbs_dir + self.event_dir)
        
        # clean up the source list from non-jpgs
        source_list = [n for n in source_list if n[-4:] == ".jpg"]
        
        # remove items that already have been resized
        if flag_redo_thumbs:
            source_to_pics_list = source_list
        else:
            source_to_pics_list = [n for n in source_list if n not in thumbs_list]
            HBFUN.verbose(str(len(source_to_pics_list)) + " of " + str(len(source_list)) + " thumbs will be resized", verbose)
    
        src_path = self.source_path + self.event_dir_src
        dest_path = self.album_path + self.thumbs_dir + self.event_dir
    

        HBFUN.make_thumbs(src_path, dest_path, source_to_pics_list, self.thumb_size, verbose)



    def get_photo_filename_from_photo_array(self):  
        """
        Will return the filenames of the photos in the array.
        """
        photo_array_fn = []
        for item in self.photo_array:
            photo_array_fn.append(item.photo_filename)
        return photo_array_fn




    def add_photos_to_array(self, verbose = False): 
        

        """
        Add photos to photo_array. It will check if they are already in there. If there are changes, it will return True, if there are no changes, it will return False.
        """
        
        HBFUN.verbose("HBevent/add_photos_to_array()", verbose)
       
        # get the list with photos already in photo_array
        photo_array_fn = self.get_photo_filename_from_photo_array()
            
        # get the list with photos
        source_list = os.listdir(self.source_path + self.event_dir_src)
        source_list = [n for n in source_list if n[-4:] == ".jpg"]
        
        # only add new photos to the array
        add_to_photo_array = [n for n in source_list if n not in photo_array_fn]
        
        if add_to_photo_array == []:
            HBFUN.verbose("  all photos are already in photo_array", verbose)
            return True 
        
        for photo_filename in add_to_photo_array:
            # read the exif. this has to be done from the source
            exif = HBFUN.get_exif(self.source_path + self.event_dir_src + photo_filename)
            # make a photo object
            ph = HBPH.photo(self.album_path, self.event_dir, photo_filename, exif)
            # add object to photo_array
            self.photo_array.append(ph)
        
        return True

    def list_photos(self):
        
        for i in range(len(self.photo_array)):
            
            if self.photo_array[i].disabled:
                disable = "D"
            else:
                disable = "-"
            
            print("  ", i, disable, self.photo_array[i].photo_filename, self.photo_array[i].photo_title)



    def make_new_properties_list(self, verbose = False):
        """
        Make a csv-file that can be used to give photos titles and captions.
        """
    
        HBFUN.verbose("HBevent/make_new_properties_list()", verbose)
    
        # get the list with photos
        source_list = os.listdir(self.source_path + self.event_dir_src)
        source_list = [n for n in source_list if n[-4:] == ".jpg"]    
    
        prop_fn = "props"
        prop_ext = "txt"
        path_and_filename = HBFUN.file_numbering(self.album_path + self.resources_dir + self.event_dir, prop_fn, prop_ext)
    
        csvfile = open(path_and_filename, "wb")
        
        csvwriter = csv.writer(csvfile, delimiter = ";")
        for i in range(len(source_list)):
            csvwriter.writerow([source_list[i], "  ", "  "])
        csvfile.close()
        
    
    def read_properties_list(self, verbose = False):
        """
        Read the csv-file with titles and captions and set the values of the photo-objects.
        """
        
        HBFUN.verbose("HBevent/read_properties_list()", verbose)
        
        photo_array_fn = self.get_photo_filename_from_photo_array()
        
        path_and_filename = self.album_path + self.resources_dir + self.event_dir + "props.txt"
        csvfile = open(path_and_filename, "rb")
        csvreader = csv.reader(csvfile, delimiter=';')
        props_list = []
        for row in csvreader:
            props_list.append(row)
    
        for i in range(len(props_list)):
            # we assume the photos are in the same order...
            self.photo_array[i].photo_title = props_list[i][1]
            self.photo_array[i].photo_caption = props_list[i][2]








        
        