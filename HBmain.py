from __future__ import print_function
from __future__ import division

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.DataClasses as DC
import Hummingbird.HBalbum as HBAl
import Hummingbird.HBhtml as HBHTML
import Hummingbird.HBfunctions as HBFun

reload(HBAl)

album_path = "/Users/robbert/Pictures/Web/"
default_source_path = "/Users/robbert/Pictures/Photos/JPG/"
pickle_path = album_path + "web.pickle"


def init_new_album():
    
    print("\nInit new album")
    
    # make new album
    album = HBAl.album(
        album_title = "Photos Robbert Bloem", 
        album_path = album_path, 
        default_source_path = default_source_path,
        verbose = True)
    
    if HBFun.ask_user_confirmation("This will overwrite the old pickle. Destroy it? y/n"):
        HBAl.save_album(album, pickle_path)

def fill_album():
    print("\nFill album")

    album = HBAl.load_album(pickle_path)    
    album.add_event(0, "Fireworks (January 2013)", "20121231_fireworks", verbose = True)
    album.add_event(1, "Berlin (July 2012)", "20120720_berlin", verbose = True)
    album.add_event(2, "Lightning (August 2011)", "20110824_lightning", verbose = True)
    HBAl.save_album(album, pickle_path)    





def add_event():
    print("\nAdd event")
    
    album = HBAl.load_album(pickle_path)  
    index = 3  
    event_title = "Summer in Zuerich"
    event_dir = "20110821_summer_weekend/"
    album.add_event(index, event_title, event_dir, verbose = True)
    HBAl.save_album(album, pickle_path)


def list_events():
    print("\nList events")
    
    album = HBAl.load_album(pickle_path)    
    album.list_events(show_photos = True)
    
def disable_event():
    print("\nDisable event")
    
    album = HBAl.load_album(pickle_path)
    album.disable_event(index = 2, disable = True, verbose = True)
    HBAl.save_album(album, pickle_path)    


def add_photos():
    
    index = 3

    album = HBAl.load_album(pickle_path)
    album.add_photos(index, flag_new_properties_list = False, flag_redo_resize = True, flag_redo_thumbs = True, verbose = True)
    HBAl.save_album(album, pickle_path)   

def make_html():
    album = HBAl.load_album(pickle_path)
    HBHTML.make_html(album, verbose = True)
    
def change_folder_thumb():
    event_index = 1
    photo_index = 10
    
    album = HBAl.load_album(pickle_path)
    album.set_folder_thumbnail(event_index, photo_index)
    HBAl.save_album(album, pickle_path)  
    


if __name__ == "__main__": 
    # init_new_album()
    # fill_album()
    # add_event()
    # disable_event()
    add_photos()
    # list_events()
    # change_folder_thumb()
    make_html()