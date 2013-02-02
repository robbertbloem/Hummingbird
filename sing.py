
import Hummingbird.HBmain as HBM


flag_verbose = True

album_path = "/Users/robbert/Pictures/Web/"
pickle_path = album_path + "web.pickle"

# # # INIT # #
# album_title = "Photos Robbert Bloem"
# default_source_path = "/Users/robbert/Pictures/Photos/JPG/"
# HBM.init_new_album(album_title, album_path, default_source_path, pickle_path, flag_verbose)
# HBM.load_events_from_csv(pickle_path, flag_verbose)

# # # ADD EVENT # #
# event_index = 0
# event_title = "Grad School retreat (Januari 2013)"
# event_dir = "20130127_grad_school_retreat/"
# event_dir_src = "20130127_grad_school_retreat/"
# source_path = ""
# HBM.add_event(pickle_path, event_index, event_title, event_dir, event_dir_src, source_path, flag_verbose)

# # # REDO RESIZING AND COPYING OF ORIGINALS # #
# event_index = 3
# redo_pics = False
# redo_thumbs = True
# HBM.redo_resize_photos(pickle_path, event_index, redo_pics = redo_pics, redo_thumbs = redo_thumbs, flag_verbose = flag_verbose)


# # # LIST EVENTS # #
# show_photos = False
# HBM.list_events(pickle_path, show_photos, flag_verbose)

# # # DISABLE EVENT # #
# event_index = 1
# disable = False
# HBM.disable_event(pickle_path, event_index, disable, flag_verbose)    

# # # DISABLE PHOTO # #
# event_index = 0
# photo_index = 0
# disable = False
# HBM.disable_photo(pickle_path, event_index, photo_index, disable, flag_verbose)   


# # # CHANGE EVENT TITLE # #
# event_index = 0
# new_title = "Grad School retreat (January 2013)"
# HBM.change_event_title(pickle_path, event_index, new_title, flag_verbose)


# # # CHANGE EVENT THUMB # #
# event_index = 0
# photo_index = 30
# HBM.change_event_thumb(pickle_path, event_index, photo_index, flag_verbose)

# # MAKE HTML # #   
HBM.make_html(pickle_path, flag_verbose = False)

