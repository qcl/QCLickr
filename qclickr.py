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

a = flickr_api.auth.AuthHandler.load('./qcl.auth')
flickr_api.set_auth_handler(a)

user = flickr_api.test.login()
print user

if __name__ == '__main__':
    print "Hello!"

