from __future__ import print_function
from __future__ import division

import os

import numpy
import matplotlib 
import matplotlib.pyplot as plt


import Hummingbird.DataClasses as DC
import Hummingbird.HBalbum as HBAL
import Hummingbird.HBevent as HBEV
import Hummingbird.HBphoto as HBPH


def make_html(album, verbose = False):

    no_nav = ""

    # make album
    f = open(album.album_path + album.html_dir + "index.html", "wb")
    make_html_header(f)
    make_html_navigation(f, album.album_title)
    gallery = prepare_album_gallery(album)
    make_html_gallery(f, gallery)
    make_html_footer(f)
    f.close()

    # make event pages
    for i in range(len(album.event_array)):

        event = album.event_array[i]

        f = open(album.album_path + album.html_dir + event.event_dir + "index.html", "wb")
        make_html_header(f, css_path = "../") 
        if i == 0:
            prev_nav = no_nav
        else:
            prev_nav = "../" + album.event_array[i-1].event_dir + "index.html"
        if i == len(album.event_array) - 1:
            next_nav = no_nav
        else:
            next_nav = "../" + album.event_array[i+1].event_dir + "index.html"        
        up_nav = "../index.html"
        make_html_navigation(f, event.event_title, prev_nav, up_nav, next_nav)
        gallery = prepare_event_gallery(event)
        make_html_gallery(f, gallery)
        make_html_footer(f)
        f.close()   


        # make photo pages
        for j in range(len(event.photo_array)):

            photo = event.photo_array[j]  
            f = open(album.album_path + album.html_dir + event.event_dir + photo.photo_html_name, "wb")      
            make_html_header(f, css_path = "../")
            if j == 0:
                prev_nav = no_nav
            else:
                prev_nav = event.photo_array[j-1].photo_html_name
            if j == len(event.photo_array) - 1:
                next_nav = no_nav
            else:
                next_nav = event.photo_array[j+1].photo_html_name
            up_nav = "index.html"
            make_html_navigation(f, event.event_title, prev_nav, up_nav, next_nav)
            make_photo_html(f, photo)
            make_html_footer(f)
            f.close()  


def make_photo_html(f, photo):

    img_path = "../../" + "pics/" + photo.event_dir + photo.photo_filename
    title = photo.photo_title
    caption = photo.photo_caption
    exif = parse_exif(photo.exif)

    f.write('<div id="photocontent">\n')
    f.write('<div id="photo">\n')
    f.write('<a href="')
    f.write(img_path)
    f.write('"><img src="')
    f.write(img_path)
    f.write('" /></a>')
    f.write('</div>\n')
    f.write('<div id="phototitle">\n')
    f.write('  <p>')
    f.write(title)
    f.write('</p>\n')
    f.write('  <p>')
    f.write(caption)
    f.write('</p>\n')
    f.write('</div>\n')
    f.write('<div id="photoprops">\n')
    f.write('  <p>')
    f.write(exif)
    f.write('</p>\n')
    f.write('</div>')
    f.write('</div>  ') 



def parse_exif(exif):

    spacer = " - "
    enter = "<br />"

    string = ""
    lens = exif['Lens']
    if lens == "Sigma Lens":
        lens = "Sigma EX 30mm 1:1.4DC"
    string += exif['Model'] + " with " + lens + " lens" + enter

    string += "Focal Length (35 mm): " + str(exif["FocalLength"][0] / exif["FocalLength"][1]) + " mm" + enter

    if exif['ExposureTime'][1] > 1:
        string += "Exposure: " + str(exif['ExposureTime'][0]) + "/" +  str(exif['ExposureTime'][1]) + " s" + spacer
    else:
        string += "Exposure: " + str(exif['ExposureTime'][0]) + " s" + spacer

    string += "Aperture F" + str(exif['FNumber'][0] / exif['FNumber'][1]) + spacer

    string += "ISO: " + str(exif["ISOSpeedRatings"])

    if exif['Copyright'] == "Robbert Bloem":
        pass
    else:
        string += entter + "Copyright: " + exif['Copyright']

    return string




def make_html_header(f, css_path = ""):

    f.write("<!DOCTYPE html>\n")
    f.write("<head>\n")
    f.write('<link rel="stylesheet" href="' + css_path + 'style.css">\n')
    f.write("</head>\n")
    f.write("<body>\n")

def make_html_navigation(f, title, prev_nav = "", up_nav = "", next_nav = ""):


    f.write('<div id="nav">\n')

    # buttons
    f.write('<div id="navbuttons">\n')
    if prev_nav:
        f.write(r'<a href="' + prev_nav + r'">&larr;</a> ')
    if up_nav:
        f.write(r' <a href="' + up_nav + r'">&uarr;</a> ')    
    if next_nav:
        f.write(r' <a href="' + next_nav + r'">&rarr;</a>')
    f.write('</div>\n')

    # title
    f.write('<div id="navtitle">\n')
    f.write(title)
    f.write('</div>\n')

    f.write('</div>\n')   


def make_html_footer(f):

    footer_text = "Copyright of site and photos: Robbert Bloem"

    f.write('<div id="footer">\n')
    f.write('  <p>')
    f.write(footer_text)
    f.write('</p>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>\n')


def make_html_gallery(f, gallery):

    n_cols = 4

    size = len(gallery)

    f.write('<div id="content">\n')
    f.write('<table>\n')

    for i in range(size):

        if i % n_cols == 0:
            f.write('<tr>\n')

        f.write('<td>\n  <div id="thumb">')
        f.write('<a href="')
        f.write(gallery[i][0])
        f.write(r'"><img src="')
        f.write(gallery[i][1])
        f.write('" /><p>\n')
        f.write(gallery[i][2])
        f.write('</p></a></div>\n</td>\n')   

        if i % n_cols == n_cols - 1 or i == size - 1:
            f.write('</tr>\n')   

    f.write('</table>\n')
    f.write('</div>\n')



def prepare_album_gallery(album):

    size = len(album.event_array)
    gallery = []
    for i in range(size):
        link = album.event_array[i].event_dir + "index.html"
        thumb_index = album.event_array[i].event_thumb
        thumb_name= album.event_array[i].photo_array[thumb_index].photo_filename
        thumb_path = "../" + album.thumbs_dir + album.event_array[i].event_dir + thumb_name
        title = album.event_array[i].event_title
        gallery += [[link, thumb_path, title]]
    return gallery


def prepare_event_gallery(event):

    size = len(event.photo_array)
    gallery = []
    for i in range(size):
        link = event.photo_array[i].photo_html_name
        thumb_path = "../../" + event.thumbs_dir + event.event_dir + event.photo_array[i].photo_filename
        title = event.photo_array[i].photo_title
        gallery += [[link, thumb_path, title]]
    return gallery       











