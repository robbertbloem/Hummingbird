from __future__ import print_function
from __future__ import division

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import Hummingbird.DataClasses as DC
import Hummingbird.HBfunctions as HBFun

class photo(DC.ClassTools):

    def __init__(self, album_path, event_dir, photo_filename, exif):

        # inherited
        self.album_path = album_path
        self.event_dir = event_dir
        self.photo_filename = photo_filename
        self.photo_html_name = HBFun.make_jpg_html(photo_filename)
        self.exif = exif

        # own            
        self._photo_title = ""
        self._photo_caption = ""
        self.disabled = False

    @property
    def photo_title(self):
        return self._photo_title
    @photo_title.setter
    def photo_title(self, text):
        self._photo_title = text.strip()

    @property
    def photo_caption(self):
        return self._photo_caption
    @photo_caption.setter
    def photo_caption(self, text):
        self._photo_caption = text.strip()