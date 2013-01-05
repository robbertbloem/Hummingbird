
import Hummingbird.HBmain as HBM


verbose = False

album_path = "/Users/robbert/Pictures/Web/"
pickle_path = album_path + "web.pickle"

# # # INIT # #
# album_title = "Photos Robbert Bloem"
# default_source_path = "/Users/robbert/Pictures/Photos/JPG/"
# 
# HBM.init_new_album(album_title, album_path, default_source_path, verbose)
# HBM.load_events_from_csv(pickle_path, verbose)

# # # ADD EVENT # #
# event_index = 1
# event_title = "Christmas Lecture (December 2012)"
# event_dir = "20121219_christmas_lecture/"
# event_dir_src = "20121219_christmas_lecture/"
# source_path = ""
# 
# HBM.add_event(pickle_path, event_index, event_title, event_dir, event_dir_src, source_path, verbose)

# # # LIST EVENTS # #
# show_photos = True
# HBM.list_events(pickle_path, show_photos, verbose)

# # # DISABLE EVENT # #
# event_index = 0
# disable = True
# HBM.disable_event(pickle_path, event_index, disable, verbose)    

# # # DISABLE PHOTO # #
# event_index = 0
# photo_index = 0
# disable = True
# HBM.disable_photo(pickle_path, event_index, photo_index, disable, verbose)   

# # CHANGE EVENT THUMB # #
event_index = 2
photo_index = 11
HBM.change_event_thumb(pickle_path, event_index, photo_index, verbose)

# # MAKE HTML # #   
HBM.make_html(pickle_path, verbose)