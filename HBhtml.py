from __future__ import print_function
from __future__ import division

import inspect
import os

import datetime
import PyRSS2Gen

import numpy
import matplotlib 
import matplotlib.pyplot as plt


import Hummingbird.DataClasses as DC
import Hummingbird.HBalbum as HBAL
import Hummingbird.HBevent as HBEV
import Hummingbird.HBphoto as HBPH
import Hummingbird.HBfunctions as HBFUN

def make_html(album, verbose = False):
    """
    make_html: the do-all function to generate html
    
    20130103/RB: started the function
    20130127/RB: generate RSS feed at end of this function
    
    INPUT:
    - album (HBAL.album)
    
    """
    
    HBFUN.verbose("make_html: Hi!", True)
    
    # some general strings
    no_nav = "" # value if there is no navigation element (first picture or so)

    # make album
    HBFUN.verbose("  make album: " + album.album_title, verbose)
    
    f = open(album.album_path + album.html_dir + "index.html", "wb")
    make_html_header(f, album.album_title)
    make_html_navigation(f, album.album_title)
    gallery = prepare_album_gallery(album)
    make_html_gallery(f, gallery)
    make_html_footer(f)
    f.close()

    # make event pages
    ev_array = range(len(album.event_array))
    ev_array = [n for n in ev_array if album.event_array[n].disabled == False]
        
    for i in ev_array: #range(len(album.event_array)):
        
        event = album.event_array[i]
        
        # filter disabled photos
        ph_array = range(len(event.photo_array))
        ph_array = [n for n in ph_array if event.photo_array[n].disabled == False]
        
        if ph_array == []:
            HBFUN.printWarning(event.event_title + " does not contain any photos or all photos are disabled. The event will be skipped!", inspect.stack())    
        
        else:
            
            event.read_properties_list(verbose)
            
            HBFUN.verbose("    make event: " + event.event_title, verbose)
            
            f = open(album.album_path + album.html_dir + event.event_dir + "index.html", "wb")
            
            page_title = album.album_title + " - " + event.event_title
            make_html_header(f, page_title, css_path = "../") 
            
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
            for j in ph_array:

                photo = event.photo_array[j]  

                HBFUN.verbose("      make photo: " + photo.photo_title, verbose)
                
                f = open(album.album_path + album.html_dir + event.event_dir + photo.photo_html_name, "wb")      
                
                page_title = album.album_title + " - " + event.event_title 
                if photo.photo_title:
                    page_title += " - " + photo.photo_title
                make_html_header(f, page_title, css_path = "../")
                
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
    
    generate_rss(album)
    
    HBFUN.verbose("make_html: Bye!", True)

    return album


def make_photo_html(f, photo):
    """
    make_photo_html: make the photo content
    
    20130103/RB: started the function
    
    """

    img_path = "../../" + "pics/" + photo.event_dir + photo.photo_filename
    title = photo.photo_title
    caption = photo.photo_caption
    exif = parse_exif(photo.exif)
    
    if title == "":
        alt_txt = photo.photo_filename
    else:
        alt_txt = title
    
    f.write('<div id="photocontent">\n')
    f.write('<div id="photo">\n')
    f.write('<a href="')
    f.write(img_path)
    f.write('"><img src="')
    f.write(img_path)
    f.write(r'" alt="')
    f.write(alt_txt)
    f.write(r'" /></a>')
    f.write('</div>\n') # end id=photo
    f.write('<div id="phototitle">\n')
    f.write('  <p>')
    f.write(title)
    f.write('</p>\n')
    f.write('  <p>')
    f.write(caption)
    f.write('</p>\n')
    f.write('</div>\n') # end id=phototitle
    f.write('<div id="photoprops">\n')
    f.write('  <p>')
    f.write(exif)
    f.write('</p>\n')
    f.write('</div>') # end id=photoprops
    f.write('</div>  ') # end id=photocontent



def parse_exif(exif):
    """
    parse_exif: turn the exif-dictionary into a nice string
    
    20130103/RB: started the function
    """
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
    
    try:
        if exif['Copyright'] == "Robbert Bloem":
            pass
        else:
            string += enter + "Copyright: " + exif['Copyright']
    except KeyError:
        pass
        

    return string




def make_html_header(f, title, css_path = ""):
    """
    make_html_header
    
    20130103/RB: started the function
    
    INPUT:
    - f (open file)
    - title (str): the title that will appear at the top of the web page
    - css_path (str): relative path to the css-file
    
    """
    f.write("<!DOCTYPE html>\n")
    f.write("<head>\n")
    f.write("<title>" + title + "</title>")
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
    f.write('<link rel="stylesheet" href="' + css_path + 'style.css">\n')
    f.write("</head>\n")
    f.write("<body>\n")

def make_html_navigation(f, title, prev_nav = "", up_nav = "", next_nav = ""):
    """
    make_html_navigation: make the navigation buttons
    
    20130103/RB: started the function
    
    INPUT:
    - f (open file)
    - title (str): title that will appear between the buttons and photo or gallery
    - prev_nav, up_nav, next_nav (str): relative path to previous, up or next photo or gallery (up is from photo to event or from event to album). An empty string will be skipped. 
    
    """

    f.write('<div id="nav">\n')

    # buttons
    f.write('<div id="navbuttons">\n')
    if prev_nav:
        f.write(r'<a href="' + prev_nav + r'">&larr;</a> ')
    if up_nav:
        f.write(r' <a href="' + up_nav + r'">&uarr;</a> ')    
    if next_nav:
        f.write(r' <a href="' + next_nav + r'">&rarr;</a>')
    f.write('</div>\n') # end id=navbuttons

    # title
    f.write('<div id="navtitle">\n')
    f.write(title)
    f.write('</div>\n') # end id=navtitle

    f.write('</div>\n') # end id=nav


def make_html_footer(f):
    """
    make_html_footer: make the footer
    
    20130103/RB: started the function
    
    """
    footer_text = 'Copyright of site and photos: Robbert Bloem'
    
    footer_links = '<a href="http://www.robbert.org">Main site</a> <a href="http://www.robbert.org/photos/album.rss">RSS-feed</a>'

    f.write('<div id="footer">\n')
    f.write('  <p>')
    f.write(footer_text)
    f.write('</p>\n')
    f.write('  <p>')
    f.write(footer_links)
    f.write('</p>\n')
    f.write('</div>\n') # end id=footer
    f.write('</body>\n')
    f.write('</html>\n')


def make_html_gallery(f, gallery):
    """
    make_html_gallery: make a gallery from a list 
    
    20130103/RB: started the function
    
    INPUT:
    - f (open file)
    - gallery (list): format has to be: [[link-url, thumbnail-url, title],..]. This is generated by prepare_album_gallery or prepare_event_gallery.
    
    REMARK:
    The point is that the album and event gallery are very similar. In a separate function all the information from the classes is ordered so this function can focus on generating html code.
    
    """
    n_cols = 4 # number of columns

    size = len(gallery)

    f.write('<div id="content">\n')
    f.write('<table>\n')

    # f.write('<div id="thumb">')

    for i in range(size):
        
        if i % n_cols == 0:
            f.write('<tr>\n') # make a new row

        f.write('<td class="thumb">\n')
        f.write('<a href="')
        f.write(gallery[i][0]) # link to event or photo
        f.write(r'"><img src="')
        f.write(gallery[i][1]) # thumbnail 
        f.write('" alt="Link to ')
        f.write(gallery[i][0])
        f.write('" /><p>\n')
        f.write(gallery[i][2]) # title
        f.write('</p></a>\n</td>\n')     

        if i % n_cols == n_cols - 1:
            f.write('</tr>\n') # end a row
    
    # f.write('</div>')
     
    string = ""
    cols_left = n_cols - size % n_cols
    if cols_left != n_cols:
        string = '<td></td>' * cols_left
        string += '</tr>\n'
    f.write(string)
            
            

    f.write('</table>\n')
    f.write('</div>\n') # end id=content



def prepare_album_gallery(album):
    """
    prepare_album_gallery: take all the events of the album and make a list used  by make_html_gallery.
    
    20130103/RB: started the function
        
    """
    # filter disabled events
    ev_array = range(len(album.event_array))
    ev_array = [n for n in ev_array if album.event_array[n].disabled == False]

    gallery = []
    for i in ev_array:
        link = album.event_array[i].event_dir + "index.html"
        thumb_index = album.event_array[i].event_thumb
        thumb_name= album.event_array[i].photo_array[thumb_index].photo_filename
        thumb_path = "../" + album.thumbs_dir + album.event_array[i].event_dir + thumb_name
        title = album.event_array[i].event_title
        gallery += [[link, thumb_path, title]]
    return gallery


def prepare_event_gallery(event):
    """
    prepare_event_gallery: take all the photos of the album and make a list used by make_html_gallery. 
    
    20130103/RB: started the function
    
    """
    # filter disabled photos
    ph_array = range(len(event.photo_array))
    ph_array = [n for n in ph_array if event.photo_array[n].disabled == False]

    gallery = []
    for i in ph_array:
        link = event.photo_array[i].photo_html_name
        thumb_path = "../../" + event.thumbs_dir + event.event_dir + event.photo_array[i].photo_filename
        title = event.photo_array[i].photo_title
        gallery += [[link, thumb_path, title]]
    return gallery       





def generate_rss(album):
    """
    generate rss: makes an rss file
    
    20130105/RB: function started
    
    REMARKS:
    The way the 'pubDate' is constructed is sensitive to mistakes, it assumes the event_dir is yyyymmdd format.
        
    http://www.dalkescientific.com/Python/PyRSS2Gen.html
    http://cyber.law.harvard.edu/rss/rss.html
    
    """
    rss_items = []
    
    web_path = "http://www.robbert.org/photos/"
    
    for i in range(len(album.event_array)):
    
        ev = album.event_array[i]
    
        ev_link = web_path + "html/" + ev.event_dir + "index.html"
    
        thumb_index = ev.event_thumb
        thumb_name = ev.photo_array[thumb_index].photo_filename
        thumb_path = web_path + album.thumbs_dir + ev.event_dir + thumb_name
    
        description = "<img src='" + thumb_path + "' />"
    
        y = int(ev.event_dir[:4])
        m = int(ev.event_dir[4:6])
        d = int(ev.event_dir[6:8])
            
        rss_items.append(PyRSS2Gen.RSSItem(
            title = ev.event_title,
            link = ev_link,
            description = description,
            guid = PyRSS2Gen.Guid(ev_link),
            pubDate = datetime.datetime(y, m, d, 0, 0)
        ))
    
    rss = PyRSS2Gen.RSS2(
        title = album.album_title,
        link = web_path + "html/index.html",
        description = album.album_title,
        lastBuildDate = datetime.datetime.utcnow(),
        items = rss_items
    )
    
    rss.write_xml(open(album.album_path + "album.rss", "w"))





