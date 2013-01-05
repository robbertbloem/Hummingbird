from __future__ import print_function
from __future__ import division

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.DataClasses as DC
import Hummingbird.HBalbum as HBAL
import Hummingbird.HBhtml as HBHTML
import Hummingbird.HBfunctions as HBFUN

reload(HBAL)

album_path = "/Users/robbert/Pictures/Web/"
default_source_path = "/Users/robbert/Pictures/Photos/JPG/"
pickle_path = album_path + "web.pickle"



def init_new_album():
    
    print("\nInit new album")
    
    # make new album
    album = HBAL.album(
        album_title = "Photos Robbert Bloem", 
        album_path = album_path, 
        default_source_path = default_source_path,
        verbose = True)
    
    if HBFUN.check_path_exists(pickle_path):
        if HBFUN.ask_user_confirmation("This will overwrite the old pickle. Destroy it? y/n"):
            HBAL.save_album(album, pickle_path)
    else:
        HBAL.save_album(album, pickle_path)




def fill_album():
    print("\nFill album")
    
    verbose = False

    album = HBAL.load_album(pickle_path)    
    album.add_event(0, "Fireworks (January 2013)", "20121231_fireworks", verbose = verbose)
    album.add_event(1, "Berlin (July 2012)", "20120720_berlin", verbose = verbose)
    album.add_event(2, "Lightning (August 2011)", "20110824_lightning", verbose = verbose)
    album.add_event(3, event_title = "Summer in Zurich (August 2011)", event_dir = "20110821_summer_zurich", event_dir_src = "20110821_summer_weekend", source_path = "", verbose = verbose)
    
    for i in range(4):
        print(album.event_array[i].event_dir_src)
        album.add_photos(i, flag_new_properties_list = False, flag_redo_resize = False, flag_redo_thumbs = False, verbose = verbose)
    
    HBAL.save_album(album, pickle_path)    





def add_event():
    print("\nAdd event")
    
    album = HBAL.load_album(pickle_path)  
    index = 4
    event_title = "Party Alexander (May 2011)"
    event_dir = "20110508_party_alex/"
    event_dir_src = "20110508a_party_alexander/"
    album.add_event(index, event_title, event_dir, event_dir_src, verbose = True)
    HBAL.save_album(album, pickle_path)


def list_events():
    print("\nList events")
    
    album = HBAL.load_album(pickle_path)    
    album.list_events(show_photos = True)
    

    
def disable_event():
    print("\nDisable event")
    
    event_index = 2
    disable = False
    
    album = HBAL.load_album(pickle_path)
    album.disable_event(index = event_index, disable = disable, verbose = True)
    HBAL.save_album(album, pickle_path)    

def disable_photo():
    print("\nDisable photo")

    event_index = 4
    photo_index = 4
    disable = False
    
    album = HBAL.load_album(pickle_path)
    album.disable_photo(event_index, photo_index, disable, verbose = True)
    HBAL.save_album(album, pickle_path)  


def add_photos():
    
    index = 4

    album = HBAL.load_album(pickle_path)
    
    album.event_array[4].event_dir_src = "20110508a_party_alexander/"
    
    album.add_photos(index, flag_new_properties_list = False, flag_redo_resize = False, flag_redo_thumbs = False, verbose = True)
    HBAL.save_album(album, pickle_path)   

def make_html():
    album = HBAL.load_album(pickle_path)
    HBHTML.make_html(album, verbose = False)
    
def change_folder_thumb():
    event_index = 1
    photo_index = 10
    
    album = HBAL.load_album(pickle_path)
    album.set_folder_thumbnail(event_index, photo_index)
    HBAL.save_album(album, pickle_path)  
    


if __name__ == "__main__": 
    # init_new_album()
    # fill_album()
    # add_event()
    # disable_event()
    disable_photo()
    # add_photos()
    # list_events()
    # change_folder_thumb()
    # make_html()
    
    