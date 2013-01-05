HUMMINGBIRD - a script to organize photos and generate an html photo album

HOW TO USE IT:

The hierarchy of classes is: album > event > photo
- HBmain contains all the functions you'll probably need. It can initialize an album, add events etc. The functions are called from sing.py.
- HBalbum has most functions in them and is used to interface with the events and photos
- HBevent and HBphoto keep track of the stuff for these classes, but you shouldn't directly call them
- HBfunctions contains some general functions.

On disk, the hierarchy is:
- album
    - pics
        - events
            - photos: photo_filename.jpg
    - thumbs
        - events
            - photos: photo_filename.jpg
    - html: index.html
        - events: event_dir_name.html
            - photos: photo_filename.html
    - res(ources): events.txt
        - events: props.txt

The reason is that you can simply copy pics/, thumbs/ and html/ to the server, while leaving res/ local. It is only used as a back up and to compile the html.


THE res/ FOLDER:

res/events.txt: its purpose is solely as a backup. If you have to reinitialize the album, you can read this file in and restore the album. You shouldn't change the file. It is really of ease-of-mind.

res/*/props.txt: this file is intended to be modified. Here you can write the properties (title, caption) of the photos. It is a csv-format with ; delimiter. Don't use that in the title or caption. The first column is the filename, the second the title, the third the caption. The props.txt file is read every time when the html is compiled.

For both cases: the files are not overwritten but get assigned a number (events_1.txt). In both cases the file without number is used (events.txt). If you want to restore an album from another file, you have to manually rename them to events.txt. 
The background is that usually you don't add photos to an event after you initially added them. Then you can give titles etc. Sometimes a new version is saved - even when no new photos are added (maybe mostly during testing) - and the script will still use the original version. If an occasional photo is added, you can manually correct the situation.
events.txt should not really be necessary to use anyway. If something goes wrong, you're probably happy to rename a file instead of having to think what you need to import.


WORKFLOW

Start album:
- run HBmain.init_new_album(..)

Add new photos:
- export photos from camera/lightroom to a folder, preferably one in the default_source_path:
    - ~/Pictures/JPG/event/
- run HBmain.add_event(..)
- give the photos some titles in */res/event/props.txt
- run HBmain.make_html()
- upload the new folders to the server
















