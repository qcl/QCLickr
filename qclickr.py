# -*- coding: utf-8 -*-
# qclickr

import sys
import os
sys.path.insert(0, os.path.join('.','lib'))

# check the api key and secret
try:
    import _config
except:
    print '''
There should be a Flickr API key and secret file _config.py which contain lines below:

API_KEY = '<API Key>'
API_SECRET = '<API Secret>'

Visit https://www.flickr.com/services/apps/ to get API key and secret
    '''
    exit()

import flickr_api

flickr_api.set_keys(api_key = _config.API_KEY, api_secret = _config.API_SECRET)

if not os.path.exists(os.path.join('.','user.auth')):
    import webbrowser
    import thread
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

    print "User auth file not found."
    oauth_verifier = None
    httpd = None
    perms = 'write'

    a = flickr_api.auth.AuthHandler(callback = "http://localhost:9487/qclickr/auth_verifier")

    def saveAuthToken(auth_verifier):
        #print 'token = ', auth_verifier
        a.set_verifier(auth_verifier)
        a.save(os.path.join('.','user.auth'))
        print 'Auth file saved.'

    class TempServerHandler(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            #print self
            #print self.headers
            #print self.path
            qclickr_verify_path = '/qclickr/auth_verifier'
            if self.path.startswith(qclickr_verify_path) and 'oauth_verifier' in self.path and '?' in self.path:
                query_str = self.path.split('?')[1]
                queries = query_str.split('&')
                for query in queries:
                    #print query
                    if '=' in query:
                        qs = query.split('=')
                        if len(qs) == 2 and qs[0] == 'oauth_verifier':
                            oauth_verifier = qs[1]
                            print 'get oauth_verifier', oauth_verifier
                            break
                if oauth_verifier != None:
                    if httpd != None:
                        self.wfile.write('QCLickr get the oauth verifier! Now you can close the page.')
                        saveAuthToken(oauth_verifier)
                        def killServer(server):
                            print 'Shut down server'
                            server.shutdown()
                        thread.start_new_thread(killServer, (httpd,))

                        return
                    else:
                        # FIXME
                        print 'Cannot found httpd'


                

    url = a.get_authorization_url(perms)
    print url

    server_address = ('', 9487)
    httpd = HTTPServer(server_address, TempServerHandler)
    print 'Start server'
    webbrowser.open_new_tab(url)
    httpd.serve_forever()

    httpd.server_close()

    exit()

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
            if filename in ['@eaDir']:  # prevent upload synology's config dir
                pass
            else:
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
    user = initAPI('./user.auth')
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

