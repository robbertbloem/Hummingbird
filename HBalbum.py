from __future__ import print_function
from __future__ import division

import csv
import inspect

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import PythonTools.ClassTools as CT
import Hummingbird.HBevent as HBEV
import Hummingbird.HBfunctions as HBFUN

reload(HBFUN)

class album(CT.ClassTools):
    """
    class album
    
    20130103/RB: started the class
    20130202/RB: uses PythonTools now for verbose, printError etc
    
    The highest class with specific photo stuff in it. ClassTools just prints the class nicely.
    
    """

    def __init__(self, album_title, album_path, default_source_path, flag_verbose = False):
        """
        __init__: start an album
        
        20130103/RB: started the function
        20130202/RB: introduced obj_id to work with PythonTools/ObjectArray
        
        INPUT:
        - album_title (str): title used for the site
        - album_path (str): the path with all the resized photos etc
        - default_source_path (str): the default path to the original photos
        
        OUTPUT:
        - True 
        """
        self.verbose("\nalbum/__init__", flag_verbose)
        
        self.obj_id = album_title
        
        self.album_title = album_title  # name of the album

        self._album_path = HBFUN.check_path(album_path, flag_verbose) 
                                        # path of the album   
        self._default_source_path = HBFUN.check_path(default_source_path, flag_verbose)
          
        self.events_csv_filename = "events"

        self._pics_dir = "pics/"        # pictures
        self._thumbs_dir = "thumbs/"    # thumbs
        self._resources_dir = "res/"    # resources
        self._html_dir = "html/"        # html

        self.event_array = []           # array with events

        self.make_folders(flag_verbose)
        

        
    # getters and setters to make sure the paths are correct
    @property
    def album_path(self):
        return self._album_path
    @album_path.setter
    def album_path(self, path):
        self._album_path = HBFUN.check_path(path)

    @property
    def default_source_path(self):
        return self._default_source_path
    @default_source_path.setter
    def default_source_path(self, path):
        self._default_source_path = HBFUN.check_path(path)

    @property
    def pics_dir(self):
        return self._pics_dir
    @pics_dir.setter
    def pics_dir(self, path):
        self._pics_dir = HBFUN.check_path(path)

    @property
    def thumbs_dir(self):
        return self._thumbs_dir
    @thumbs_dir.setter
    def thumbs_dir(self, path):
        self._thumbs_dir = HBFUN.check_path(path) 

    @property
    def resources_dir(self):
        return self._resources_dir
    @resources_dir.setter
    def resources_dir(self, path):
        self._resources_dir = HBFUN.check_path(path)

    @property
    def html_dir(self):
        return self._html_dir
    @html_dir.setter
    def html_dir(self, path):
        self._html_dir = HBFUN.check_path(path)

    
    def make_folders(self, flag_verbose = False):
        """
        make_folders: create the web-folders
        
        20130103/RB: started the function
        20130202/RB: change to PythonTools, will now also make the album_path itself, not only its subfolders
        
        INPUT:
        None
        
        OUTPUT:
        - True: success, or False: failure
        """
        self.verbose("\nHBalbum/make_folders()", flag_verbose)
        
        if self.album_path == self._default_source_path:
            self.printError("album_path and default_source_path are the same, this is not allowed!", inspect.stack())
            return False
        
        HBFUN.check_and_make_folder(self.album_path, flag_verbose)
        
        path = self.album_path + self.pics_dir
        HBFUN.check_and_make_folder(path, flag_verbose)
        
        path = self.album_path + self.thumbs_dir
        HBFUN.check_and_make_folder(path, flag_verbose)
        
        path = self.album_path + self.resources_dir
        HBFUN.check_and_make_folder(path, flag_verbose)
                
        path = self.album_path + self.html_dir
        HBFUN.check_and_make_folder(path, flag_verbose)  
        
        return True      
    

    def add_event(self, index, event_title, event_dir, event_dir_src = "", source_path = "", flag_verbose = False):
        """
        add_event: add an event to the album
        
        20130103/RB: started the function
        
        INPUT:
        - index (int): position of the new album. Use 'list_events' to find the correct position. The newest event should have index = 0
        - event_title (str): the title of the event. It usually has the format 'Some event (July 2012)'
        - event_dir (str): the directory name of the event on the web
        - event_dir_src (str, opt): if the source directory (with the original photos) has a different directory name
        - source_path (str, opt): is the source_path of the original photos is not the default.

        OUTPUT:
        - True: success or False: fail 
        
        """
           
        self.verbose("HBalbum/add_event(): " + str(index) + ", " + event_title + ", " + event_dir + ", " + source_path, flag_verbose)
        
        # if no new source_path is given, use the default
        if source_path == "":
            source_path = self.default_source_path
        # if a new source_path is given, check for correctness
        else:
            source_path = HBFUN.check_path(source_path, flag_verbose)
            if self.album_path == source_path:
                self.printError("album_path and source_path are the same, this is not allowed!", inspect.stack())
                return False
        
        # check the event_dir
        event_dir = HBFUN.check_path(event_dir)
        
        # is the source event dir different?
        if event_dir_src == "":
            event_dir_src = event_dir
        else:
            event_dir_src = HBFUN.check_path(event_dir_src, flag_verbose)
            
        # check if the source exists
        if HBFUN.check_path_exists(source_path + event_dir_src) == False:
            self.printError("The source path does not exist!", inspect.stack())
            return False            
              
        # check if the event already exists. If not, make it
        if self.check_event_exists(event_title, event_dir, flag_verbose):
            ev = HBEV.event(event_title, event_dir, event_dir_src, self.album_title, self.album_path, source_path, self.pics_dir, self.thumbs_dir, self.resources_dir, self.html_dir, flag_verbose)
            self.event_array.insert(index, ev)
        
        self.save_events_in_csv(flag_verbose)
        
        return True






    def check_event_exists(self, event_title, event_dir, flag_verbose = False):
        """
        check_event_exists
        
        20130103/RB: started function
        
        INPUT:
        - event_title (str): the title of the event. It usually has the format 'Some event (July 2012)'
        - event_dir (str): the directory name of the event on the web 
        
        OUTPUT:
        - True: if it does not exist, False if it does exist
        """
        
        self.verbose("HBalbum/check_event_exists(): " + event_title + ", " + event_dir, flag_verbose)
        
        ev_titles = []
        ev_dirs = []

        for i in range(len(self.event_array)):
            ev_titles.append(self.event_array[i].event_title)
            ev_dirs.append(self.event_array[i].event_dir)

        if event_title in ev_titles:
            self.printError("the event_title does already exist!", inspect.stack())
            return False
        elif event_dir in ev_dirs:
            self.printError("the event_dir does already exist!", inspect.stack())
            return False
        else:
            self.verbose("  HBalbum/check_event_exists(): event_title and event_dir do not yet exist", flag_verbose)
            return True



    
    def list_events(self, show_photos = False, flag_verbose = False):
        """
        list_events: prints a list with all events in the album. Disabled events and photos are marked with a 'D'
        
        20130103/RB: started the function
        
        INPUT:
        show_photos (BOOL, False): also show the photos in the events
        
        """
        self.verbose("List events", flag_verbose)
        
        for i in range(len(self.event_array)):
            
            if self.event_array[i].disabled:
                disable = "D"
            else:
                disable = "-"
            
            print(i, disable, self.event_array[i].event_title, self.event_array[i].event_dir)
            
            if show_photos:
                self.event_array[i].list_photos()
                
            
    
    def disable_event(self, index, disable, flag_verbose = False):
        """
        disable_event: disable or enable an event. 
        
        20130103/RB: started function
        
        INPUT:
        - index (int): index of the event in event_array. Use 'list_events' to find the correct index. If index is -1, it will affect all albums.
        - disable (BOOL): True to disable, False to enable. If you try to re-disable an event, it will give a warning and continue
        
        OUTPUT:
        - True: success or False: failure
        
        """
        
        ev = ev = self.event_array[index]
        
        if disable:
            dis = "disabled"
        else:
            dis = "enabled"

        self.verbose("HBalbum/disable_event(): index " + str(index) + " to " + dis, flag_verbose)

        if index > len(self.event_array) or index < -1:
            HBFUN.printError("The index exceeds the length of the array", inspect.stack())
            return False
            
        if index == -1:
            self.verbose("  all events will be set to " + dis, flag_verbose)
            for i in range(len(self.event_array)):
                ev.disabled = disable
        
        else:
            if ev.disabled == disable:
                self.printWarning("Event " + ev.event_title + " is already " + dis, inspect.stack())
            
            self.verbose("  event_title: " + ev.event_title, flag_verbose)
            self.verbose("  event_dir: " + ev.event_dir, flag_verbose)          
            ev.disabled = disable
        
        return True


    def disable_photo(self, event_index, photo_index, disable, flag_verbose = False):
        """
        disable_photo: disable or enable an event. 
        
        20130103/RB: started function
        
        INPUT:
        - event_index (int): index of the event in event_array. Use 'list_events' to find the correct index.
        - disable (BOOL): True to disable, False to enable. If you try to re-disable an event, it will give a warning and continue
        
        OUTPUT:
        - True: success or False: failure
        
        """
        # use a bit of shorthand... sorry
        ev = self.event_array[event_index]
        ph = ev.photo_array[photo_index]
        
        if disable:
            dis = "disabled"
        else:
            dis = "enabled"
    
        self.verbose("HBalbum/disable_photo(): event " + ev.event_title + " photo " + ph.photo_filename + " to " + dis, flag_verbose)
    
        if event_index > len(self.event_array):
            self.printError("The event index exceeds the length of the event_array", inspect.stack())
            return False

        if photo_index > len(ev.photo_array):
            self.printError("The photo_index exceeds the length of the photo_array", inspect.stack())
            return False

           
        if ph.disabled == disable:
            self.printWarning("Event " + ev.event_title + " photo " + ph.photo_filename + " is already " + dis, inspect.stack())

        self.verbose("  event_title: " + ev.event_title, flag_verbose)
        self.verbose("  event_dir: " + ev.event_dir, flag_verbose)           
        self.verbose("  photo_title: " + ph.photo_title, flag_verbose)
        self.verbose("  photo_filename: " + ph.photo_filename, flag_verbose)  
                
        ph.disabled = disable
        
        return True



    def set_folder_thumbnail(self, event_index, photo_index, flag_verbose = False):
        """
        set_folder_thumbnail: change the thumbnail used for an event
        
        20130103/RB: started function
        
        INPUT:
        - event_index (int): index of the event in event_array. Use 'list_events' with 'show_photos = True' to find the correct index.
        - photo_index (int): index if the photo used for the thumbnail       
        
        OUTPUT:
        - True: success, False: the one of the indices does not exist.
        
        """
        
        try:
            self.verbose("set_folder_thumbnail, event: " + str(event_index) + " photo: " + str(photo_index), flag_verbose)
            self.event_array[event_index].photo_array[photo_index]
        except IndexError:
            self.printError("Either the event_index or photo_index is incorrect", inspect.stack())
            return False
        
        self.event_array[event_index].event_thumb = photo_index

        self.save_events_in_csv(flag_verbose)

        return True


    def add_photos(self, index, flag_new_properties_list = False, flag_redo_resize = False, flag_redo_thumbs = False, flag_verbose = False):
        """
        add_photos: add photos to an event
        
        20130103/RB: started function
        
        INPUT:
        - index (int): index of the event in event_array. Use 'list_events' to find the correct index.
        - flag_new_properties_list (BOOL, False): complicated. The properties list is a csv-file with the file names and space for titles and caption for individual photos. You don't want to override it. The file is found in 'album_path + resources_dir + event_dir + 'props.csv''
            - if the file does not exist, it will be made
            - if the file exists and the flag is False, it will not make a new one
            - if the file exists and the flag is True, it will make a new file, with a number appended to it (like 'props_1.csv'). THE OLD FILE WILL CONTINUE TO BE USED. You have to manually rename it to 'props.csv'.
        - flag_redo_resize (BOOL, False): the photos are copied from the source, resize and put in the destination folder. During this, the exif information is copied to the resized photos.
            - no photos found in destination: will always resize them
            - photos are found, flag is False: will not do anything
            - photos are found, flag is True: will resize the photos
        - flag_redo_thumbs (BOOL, False): similar to flag_redo_resize, but for the thumbnails.
        
        REMARK:
        This function is a convenient collection of steps. Error checking etc should be done in the respective functions.
        
        """

        self.verbose("\nHBalbum/add_photos(): redo resize: " + str(flag_redo_resize), flag_verbose)
        
        self.event_array[index].add_and_resize_photos(flag_redo_resize, flag_verbose)
        self.event_array[index].add_and_resize_thumbs(flag_redo_thumbs, flag_verbose)
        self.event_array[index].add_photos_to_array(flag_verbose)
        
        if HBFUN.check_path_exists(self.album_path + self.resources_dir + self.event_array[index].event_dir) or flag_new_properties_list:
            self.event_array[index].make_new_properties_list(flag_verbose)
            
        self.event_array[index].read_properties_list(flag_verbose)


    def save_events_in_csv(self, flag_verbose = False):
        """
        
        
        20130105/RB: started the function
        
        
        """
        self.verbose("HBalbum/save_events_in_csv()", flag_verbose)
        
        # create a save filename
        prop_ext = "txt"
        path_and_filename = HBFUN.file_numbering(self.album_path + self.resources_dir, self.events_csv_filename, prop_ext)
        
        # write the properties
        csvfile = open(path_and_filename, "wb")
        csvwriter = csv.writer(csvfile, delimiter = ";")
        for i in range(len(self.event_array)):
            ev = self.event_array[i]
            csvwriter.writerow([i, ev.event_title, ev.event_dir, ev.event_dir_src, ev.source_path, ev.event_thumb])
        csvfile.close()


    def load_events_from_csv(self, flag_verbose = False):
        """
        
        
        20130105/RB: started the function
        
        
        """
        
        self.verbose("HBalbum/load_events_in_csv()", flag_verbose)
        
        path_and_filename = self.album_path + self.resources_dir + self.events_csv_filename + ".txt"
        csvfile = open(path_and_filename, "rb")
        csvreader = csv.reader(csvfile, delimiter=';')
        temp_ev_list = []
        for row in csvreader:
            temp_ev_list.append(row)
    
        for i in range(len(temp_ev_list)):
            self.add_event(
                index = int(temp_ev_list[i][0]), 
                event_title = temp_ev_list[i][1], 
                event_dir = temp_ev_list[i][2], 
                event_dir_src = temp_ev_list[i][3], 
                source_path = temp_ev_list[i][4], 
                flag_verbose = flag_verbose)
            
        for i in range(len(temp_ev_list)):
            self.add_photos(
                index = int(temp_ev_list[i][0]), 
                flag_new_properties_list = False, 
                flag_redo_resize = False, 
                flag_redo_thumbs = False, 
                flag_verbose = flag_verbose)
            
            self.set_folder_thumbnail(int(temp_ev_list[i][0]), int(temp_ev_list[i][5]))


    def change_event_title(self, event_index, new_title, flag_verbose = False):
        """
        change_event_title: change the title
        
        20130127/RB: wrote this function
        
        """
        
        self.verbose("HBalbum/change_event_title()", flag_verbose)
 
        self.event_array[event_index].event_title = new_title
        
        return True
        






    
    