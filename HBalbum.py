from __future__ import print_function
from __future__ import division

import inspect

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.DataClasses as DC
import Hummingbird.HBevent as HBEv
import Hummingbird.HBfunctions as HBFun

reload(HBFun)

def save_album(album, pickle_path, flag_overwrite = False):
    DC.make_db([album], pickle_path, flag_overwrite)
    
def load_album(pickle_path):
    return DC.import_db(pickle_path)[0]


class album(DC.ClassTools):

    def __init__(self, album_title, album_path, default_source_path, verbose = False):

        HBFun.verbose("\nalbum/__init__", verbose)

        self.album_title = album_title  # name of the album

        self._album_path = HBFun.check_path(album_path, verbose) 
                                        # path of the album   
        self._default_source_path = HBFun.check_path(default_source_path, verbose)  
                                        # default source of photos 
        self._pics_dir = "pics/"        # pictures
        self._thumbs_dir = "thumbs/"    # thumbs
        self._resources_dir = "res/"    # resources
        self._html_dir = "html/"        # html

        self.event_array = []           # array with events

        self.make_folders(verbose)
        

    @property
    def album_path(self):
        return self._album_path
    @album_path.setter
    def album_path(self, path):
        self._album_path = HBFun.check_path(path)

    @property
    def default_source_path(self):
        return self._default_source_path
    @default_source_path.setter
    def default_source_path(self, path):
        self._default_source_path = HBFun.check_path(path)

    @property
    def pics_dir(self):
        return self._pics_dir
    @pics_dir.setter
    def pics_dir(self, path):
        self._pics_dir = HBFun.check_path(path)

    @property
    def thumbs_dir(self):
        return self._thumbs_dir
    @thumbs_dir.setter
    def thumbs_dir(self, path):
        self._thumbs_dir = HBFun.check_path(path) 

    @property
    def resources_dir(self):
        return self._resources_dir
    @resources_dir.setter
    def resources_dir(self, path):
        self._resources_dir = HBFun.check_path(path)

    @property
    def html_dir(self):
        return self._html_dir
    @html_dir.setter
    def html_dir(self, path):
        self._html_dir = HBFun.check_path(path)

    
    def make_folders(self, verbose = False):
        """
        Create the web-folders
        """
        HBFun.verbose("\nHBalbum/make_folders()", verbose)
        
        if self.album_path == self._default_source_path:
            HBFun.printError("album_path and default_source_path are the same, this is not allowed!", inspect.stack())
            return False
        
        path = self.album_path + self.pics_dir
        HBFun.check_and_make_folder(path, verbose)
        
        path = self.album_path + self.thumbs_dir
        HBFun.check_and_make_folder(path, verbose)
        
        path = self.album_path + self.resources_dir
        HBFun.check_and_make_folder(path, verbose)
                
        path = self.album_path + self.html_dir
        HBFun.check_and_make_folder(path, verbose)  
        
        return True      
    

    def add_event(self, index, event_title, event_dir, event_dir_src = "", source_path = "", verbose = False):
        
        HBFun.verbose("HBalbum/add_event(): " + str(index) + ", " + event_title + ", " + event_dir + ", " + source_path, verbose)
        
        # if no new source_path is given, use the default
        if source_path == "":
            source_path = self.default_source_path
        # if a new source_path is given, check for correctness
        else:
            source_path = HBFun.check_and_make_folder(source_path, verbose)
            if self.album_path == source_path:
                HBFun.printError("album_path and source_path are the same, this is not allowed!", inspect.stack())
                return False
        
        # check the event_dir
        event_dir = HBFun.check_path(event_dir)
        
        if event_dir_src == "":
            event_dir_src = event_dir
        else:
            event_dir_src = HBFun.check_and_make_folder(event_dir_src, verbose)
        

        # check if the event already exists. If not, make it
        if self.check_event_exists(event_title, event_dir, verbose):
            ev = HBEv.event(event_title, event_dir, event_dir_src, self.album_title, self.album_path, source_path, self.pics_dir, self.thumbs_dir, self.resources_dir, self.html_dir, verbose)
            self.event_array.insert(index, ev)
        
        return True






    def check_event_exists(self, event_title, event_dir, verbose = False):
        
        HBFun.verbose("HBalbum/check_event_exists(): " + event_title + ", " + event_dir, verbose)
        
        ev_titles = []
        ev_dirs = []

        for i in range(len(self.event_array)):
            ev_titles.append(self.event_array[i].event_title)
            ev_dirs.append(self.event_array[i].event_dir)

        if event_title in ev_titles:
            HBFun.printError("the event_title does already exist!", inspect.stack())
            return False
        elif event_dir in ev_dirs:
            HBFun.printError("the event_dir does already exist!", inspect.stack())
            return False
        else:
            HBFun.verbose("  HBalbum/check_event_exists(): event_title and event_dir do not yet exist", verbose)
            return True



    
    def list_events(self, show_photos = False):
        
        for i in range(len(self.event_array)):
            
            if self.event_array[i].disabled:
                disable = "D"
            else:
                disable = "-"
            
            print(i, disable, self.event_array[i].event_title, self.event_array[i].event_dir)
            
            if show_photos:
                self.event_array[i].list_photos()
                
            
    
    def disable_event(self, index, disable, verbose = False):

        if disable:
            dis = "disabled"
        else:
            dis = "enabled"

        HBFun.verbose("HBalbum/disable_event(): index " + str(index) + " to " + dis, verbose)

        if index > len(self.event_array) or index < -1:
            HBFun.printError("The index exceeds the length of the array", inspect.stack())
            return False
            
        if index == -1:
            HBFun.verbose("  all events will be set to " + dis, verbose)
            for i in range(len(self.event_array)):
                self.event_array[i].disabled = disable
        
        else:
            HBFun.verbose("  event_title: " + self.event_array[index].event_title, verbose)
            HBFun.verbose("  event_dir: " + self.event_array[index].event_dir, verbose)          
            self.event_array[index].disabled = disable



    def set_folder_thumbnail(self, event_index, photo_index):
        
        self.event_array[event_index].event_thumb = photo_index


    def add_photos(self, index, flag_new_properties_list = False, flag_redo_resize = False, flag_redo_thumbs = False, verbose = False):
        
        HBFun.verbose("\nHBalbum/add_photos(): redo resize: " + str(flag_redo_resize), verbose)
        
        self.event_array[index].add_and_resize_photos(flag_redo_resize, verbose)
        self.event_array[index].add_and_resize_thumbs(flag_redo_thumbs, verbose)
        self.event_array[index].add_photos_to_array(verbose)
        
        if flag_new_properties_list:
            self.event_array[index].make_new_properties_list(verbose)
            
        self.event_array[index].read_properties_list(verbose)










 
    
    
    