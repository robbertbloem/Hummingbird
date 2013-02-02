"""

<O   /
  WWW
   |

"""


from __future__ import print_function
from __future__ import division

import numpy
import matplotlib 
import matplotlib.pyplot as plt

# import Hummingbird.DataClasses as DC
import PythonTools.ObjectArray as OA
import PythonTools.Debug as DEBUG
import Hummingbird.HBalbum as HBAL
import Hummingbird.HBhtml as HBHTML
import Hummingbird.HBfunctions as HBFUN

reload(HBAL)





def init_new_album(album_title, album_path, default_source_path, pickle_path, flag_verbose = False):
    """
    init_new_album: start or restart an album
    
    20130103/RB: started function
    
    INPUT:
    - album_title: title of the page (as seen on the web page)
    - album_path: path to where the album is located on the computer
    - default_source_path: the default path to the folder with the originals
    
    INTERACTION:
    - the album will be saved. If it already exists it will ask for confirmation before it overwrites the old album.
    """
    DEBUG.verbose("== INIT NEW ALBUM ==", True)
    
    # make new album
    album = HBAL.album(album_title = album_title, album_path = album_path, default_source_path = default_source_path, verbose = verbose)
    
    # save it, if it already exists, ask for confirmation
    if HBFUN.check_path_exists(pickle_path):
        if HBFUN.ask_user_confirmation("This will overwrite the old pickle. Destroy it? y/n"):
            oa = OA.objectarray("album", "album")
            oa.add_object(album)
            oa.save_objectarray(pickle_path, flag_overwrite = True)
    else:
        save_album(album, pickle_path)



def load_album(pickle_path, flag_verbose = False):
    oa = OA.objectarray("object_array", "object_array", flag_verbose = flag_verbose)  
    oa.import_db(pickle_path, flag_verbose = flag_verbose)
    return oa.obj_array[0]

def save_album(album, pickle_path, flag_verbose = False):
    oa = OA.objectarray("object_array", "object_array", flag_verbose = flag_verbose)
    oa.add_object(album, flag_verbose = flag_verbose)
    oa.save_objectarray(pickle_path, flag_overwrite = flag_verbose)  


def load_events_from_csv(pickle_path, flag_verbose = False):
    """
    load_events_from_csv: should only be used if you had to re-init an album
    
    20130105/RB: started function
    
    INPUT:
    - events_csv_filename (str): the filename, without extension, of the csv file. Warning: save_file_in_csv will number filenames!
    - pickle_path: path and filename of the pickle
    
    """
    DEBUG.verbose("load_events_from_csv", flag_verbose)
    
    album = load_album(pickle_path)
    album.load_events_from_csv(flag_verbose)
    save_album(album, pickle_path)
    



def add_event(pickle_path, event_index, event_title, event_dir, event_dir_src = "", source_path = "", flag_verbose = False):
    """
    add_event: add an event to the album and add the photos to the event
    
    20130103/RB: started function

    INPUT:
    - pickle_path (str): path and filename of the pickle
    - index (int): position of the new album. Use 'list_events' to find the correct position. The newest event should have index = 0
    - event_title (str): the title of the event. It usually has the format 'Some event (July 2012)'
    - event_dir (str): the directory name of the event on the web
    - event_dir_src (str, opt): if the source directory (with the original photos) has a different directory name
    - source_path (str, opt): if the source_path of the original photos is not the default.   
    """
    
    DEBUG.verbose("Add event", flag_verbose)
    
    album = load_album(pickle_path)  
    album.add_event(event_index, event_title, event_dir, event_dir_src, source_path = source_path, flag_verbose = flag_verbose)
    album.add_photos(event_index, flag_new_properties_list = False, flag_redo_resize = False, flag_redo_thumbs = False, flag_verbose = flag_verbose)
    save_album(album, pickle_path)


def list_events(pickle_path, show_photos = False, flag_verbose = False):
    """
    list_events: list events, and maybe also photos
    
    20130103/RB: started function
    
    INPUT:
    - pickle_path (str): path and filename of the pickle
    - show_photos (BOOL, False): if True, it will also list the photos 
    """
    DEBUG.verbose("List events", flag_verbose)
    
    album = load_album(pickle_path)    
    album.list_events(show_photos)
    

    
def disable_event(pickle_path, event_index, disable, flag_verbose = False):
    """
    disable_event: disable an event. This will exclude it from the events gallery, but it will not remove the html code itself
    
    20130103/RB: started function

    - event_index (int): index of the event in event_array. Use 'list_events' to find the correct index. If index is -1, it will affect all albums.
    - disable (BOOL): True to disable, False to enable. If you try to re-disable an event, it will give a warning and continue    
    """
    DEBUG.verbose("Disable event", flag_verbose)
    
    album = load_album(pickle_path)
    album.disable_event(index = event_index, disable = disable, flag_verbose = flag_verbose)
    save_album(album, pickle_path)    


def disable_photo(pickle_path, event_index, photo_index, disable, flag_verbose = False):
    """
    disable_photo: see disable_event for info
    
    20130103/RB: started function
    
    """
    DEBUG.verbose("Disable photo", flag_verbose)
    
    album = load_album(pickle_path)
    album.disable_photo(event_index, photo_index, disable, flag_verbose = flag_verbose)
    save_album(album, pickle_path)  





def make_html(pickle_path, flag_verbose = False):
    """
    make_html: compile the html
    
    20130103/RB: started function
    
    """
    DEBUG.verbose("Make html", flag_verbose)
    
    album = load_album(pickle_path)
    album = HBHTML.make_html(album, flag_verbose = flag_verbose)
    save_album(album, pickle_path) # to save the newly imported properties


def change_event_thumb(pickle_path, event_index, photo_index, flag_verbose = False):
    """
    change_event_thumb: change the thumbnail used for the event
    
    20130103/RB: started function
    
    INPUT:
    - event_index (int): a valid index of an event
    - photo_index: a valid index of a photo
    
    """
    DEBUG.verbose("Change event thumbnail", flag_verbose)
    
    album = load_album(pickle_path)
    album.set_folder_thumbnail(event_index, photo_index)
    save_album(album, pickle_path)  

def change_event_title(pickle_path, event_index, new_title, flag_verbose = False):
    
    DEBUG.verbose("Change event title", flag_verbose)
    
    album = load_album(pickle_path)
    album.change_event_title(event_index, new_title)
    save_album(album, pickle_path)    

def save_events_in_csv(pickle_path, flag_verbose = False):
    """
    save_events_in_csv: if you want to specifically save a csv file... this is done automatically, so no real need to use this function
    
    20130105/RB: started function
    
    INPUT:
    - pickle_path
    - events_csv_filename (str): a filename, without extension, where the csv is saved. It will not overwrite older files, instead they will be numbered.
    
    """
    album = load_album(pickle_path)
    album.save_events_in_csv(flag_verbose)

def redo_resize_photos(pickle_path, event_index, redo_pics = False, redo_thumbs = False, flag_verbose = False):
    """
    redo_resize_photos: if needed, you can redo the resizing of the photos.
    
    20130105/RB: started function
    
    INPUT:
    - pickle_path
    - event_index
    - redo_pics
    - redo_thumbs
    
    """

    album = load_album(pickle_path)
    album.add_photos(event_index, flag_new_properties_list = False, flag_redo_resize = redo_pics, flag_redo_thumbs = redo_thumbs, flag_verbose = flag_verbose)
    save_album(album, pickle_path) 

if __name__ == "__main__": 

    # album_path = "/Users/robbert/Pictures/Web/"
    # pickle_path = album_path + "web.pickle"
    # 
    # album = HBAL.load_album(pickle_path)
    # HBHTML.generate_rss(album)

    pass
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    