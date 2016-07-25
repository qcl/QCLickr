# -*- coding: utf-8 -*-
# qclickr

import sys
import os
sys.path.insert(0, os.path.join('.','lib'))

import _config
import flickr_api

flickr_api.set_keys(api_key = _config.API_KEY, api_secret = _config.API_SECRT)
#perms = 'write'
#
#a = flickr_api.auth.AuthHandler()
#url = a.get_authorization_url(perms)
#print url

#a = flickr_api.auth.AuthHandler.load('./qcl.auth')
#flickr_api.set_auth_handler(a)

#user = flickr_api.test.login()
#print user

photosets = []
photosetDict = {}

def initAPI(auth_filename):
    a = flickr_api.auth.AuthHandler.load(auth_filename)
    flickr_api.set_auth_handler(a)
    user = flickr_api.test.login()
    print 'Hi,',user.username
    print 'Building photo sets...'
    photosets = user.getPhotosets()
    for photoset in photosets:
        #print photoset.title
        photosetDict[photoset.title] = photoset
    return user

def uploadDir(path):
    print 'Prepare to upload dir', path
    photos = os.listdir(path)
    dirname = os.path.basename(path)
    if dirname == '':
        dirname = os.path.basename(os.path.dirname(path))
    albumName = dirname
    for filename in photos:
        filepath = os.path.join(path, filename)
        i += 1
        if os.path.isfile(filepath):
            uploadPhoto(filepath, newAlbum = True)
            print i,'/',len(photos)
        elif os.path.isdir(filepath):
            uploadDir(filepath)
            currentPhotosetsPhotos['photos'] = []
        else:
            pass

def createNewAlbum(albumName, photo):
    if not albumName in photosetDict:
        photoset = flickr_api.Photoset.create(title = albumName, primary_photo_id = photo.id)
        photosetDict[albumName] = photoset
        return photoset
    else:
        return photosetDict[albumName]

def uploadPhoto(filename, newAlbum = False):
    if not filename[-4:] in ['.jpg', 'jpeg', '.JPG', 'JPEG', '.png', '.PNG']:
        print 'Not a image'
        return

    dirname = os.path.basename(os.path.dirname(filename))
    print 'Prepare to upload', filename
    print 'Which is based in', dirname

    photo = flickr_api.upload(photo_file = filename, is_public = 0, is_friend = 0, is_family = 0)
    print 'Uploaded', photo
    if dirname in photosetDict:
        photoset = photosetDict[dirname]
        photoset.addPhoto(photo = photo)
        print 'Add photo', photo, 'into', photoset 
    elif newAlbum:
        photoset = createNewAlbum(dirname, photo)
        print 'Add photo', photo, 'into', photoset 

def uploadPhotos(path):
    user = initAPI('./qcl.auth')
    if os.path.isdir(path) :
        uploadDir(path)
    elif os.path.exists(path):
        uploadPhoto(path)
    else:
        print path,'doestn\'t exist'

if __name__ == '__main__':
    print "QCLickr"
    if len(sys.argv) > 1:
        uploadPhotos(sys.argv[1])
    else:
        print '$ python qclickr.py [file|dir]'

