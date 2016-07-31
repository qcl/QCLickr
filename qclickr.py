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
currentPhotosetsPhotos = {}

def initAPI(auth_filename):
    a = flickr_api.auth.AuthHandler.load(auth_filename)
    flickr_api.set_auth_handler(a)
    user = flickr_api.test.login()
    print 'Hi,',user.username
    print 'Building photo sets...'
    w = flickr_api.Walker(user.getPhotosets)
    #photosets = user.getPhotosets()
    #print photosets.info
    for photoset in w:
        #print photoset.title
        photosetDict[photoset.title] = photoset
    return user

def uploadDir(path):
    print 'Prepare to upload dir', path
    photos = os.listdir(path)
    dirname = os.path.basename(path)
    if dirname == '':
        dirname = os.path.basename(os.path.dirname(path))
    if type(dirname) == type('string'): # make sure dirname is always unicode str
        dirname = dirname.decode('utf-8')
    albumName = dirname

    currentPhotosetsPhotos['title'] = dirname
    currentPhotosetsPhotos['photos'] = {}

    photos.sort()
    i = 0
    for filename in photos:
        filepath = os.path.join(path, filename)
        i += 1
        if os.path.isfile(filepath):
            print '#',i
            uploadPhoto(filepath, newAlbum = True)
            print i,'/',len(photos)
            print ''
        elif os.path.isdir(filepath):
            uploadDir(filepath)
            currentPhotosetsPhotos['photos'] = {}
        else:
            pass

def createNewAlbum(albumName, photo):
    if not albumName in photosetDict:
        print 'Prepare to create new album', albumName
        if type(albumName) == type(u'字串'):
            albumName = albumName.encode('utf-8')
        photoset = flickr_api.Photoset.create(title = albumName, primary_photo_id = photo.id)
        photosetDict[photoset.title] = photoset
        print 'Already created', photoset
        return photoset
    else:
        return photosetDict[albumName]

def uploadPhoto(filename, newAlbum = False):
    if not filename[-4:] in ['.jpg', 'jpeg', '.JPG', 'JPEG', '.png', '.PNG']:
        print 'Not a image'
        print 'Skip', filename
        return

    dirname = os.path.basename(os.path.dirname(filename))
    print 'Prepare to upload', filename
    print 'Which is based in', dirname

    if type(dirname) == type('string'):
        dirname = dirname.decode('utf-8')

    #print currentPhotosetsPhotos
    if len(currentPhotosetsPhotos['photos']) == 0 and dirname in photosetDict:
        photoset = photosetDict[dirname]
        print "Building photos' info in album", dirname
        #photos = photoset.getPhotos()
        w = flickr_api.Walker(photoset.getPhotos)
        for photo in w:
            if len(photo.title) > 0:
                #print photo.title
                currentPhotosetsPhotos['photos'][photo.title] = photo
            else:
                pass

    title = os.path.basename(filename)
    if title[-4] == ".":
        title = title[:-4]
    elif title[-5] == '.':
        title = title[:-5]
    else:
        title = title.split('.')[0]
    title = title.decode('utf-8')
    if title in currentPhotosetsPhotos['photos']:
        print 'Already uploaded. Skip',title
    else:
        print 'Uploading', title
        photo = flickr_api.upload(photo_file = filename, is_public = 0, is_friend = 0, is_family = 0)
        print 'Uploaded', photo

        if dirname in photosetDict:
            photoset = photosetDict[dirname]
            photoset.addPhoto(photo = photo)
            print 'Add photo', photo, 'into', photoset
        elif newAlbum:
            photoset = createNewAlbum(dirname, photo)
            print 'Add photo', photo, 'into', photoset

        currentPhotosetsPhotos['photos'][photo.title] = photo

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

