from __future__ import print_function

import requests
from os.path import splitext
from hashlib import sha1

from .config import vimimg, existdb

class Vimcn:
    def __init__(self, file):
        self._ext = ''
        self.existdb = existdb
        if (hasattr(file, 'decode')):
            # If the file type is bytes then the file is the content
            self.content = file
        elif (hasattr(file, 'read')):
            # if it is an already opened file then the content is to read
            self.content = f.read()
        else:
            # If it is a file name then open it
            self.name, self._ext = splitext(file)
            with open(file, 'rb') as f:
                self.content = f.read()

        # Calculate the hash
        self.hash = sha1(self.content)
        self.ok = False

    # Extension of the file
    @property
    def ext(self):
        return self._ext

    @ext.setter
    def ext(self, x):
        self._ext = x

    def url(self, ext=None):
        ext = self.ext or ''
        digest = self.hash.hexdigest()
        # https://img.vim-cn.com/[digest0-2]/[digest3-32].ext
        result = vimimg + digest[:2] + "/" + digest[2:] + ext
        return result

    # Write the file to exist db
    def _cache_exist(self):
        self.existdb[self.hash.hexdigest()] = 1

    # Check if the file exist in db
    def _exist(self):
        if self.ok:
            return True
        return self.hash.hexdigest() in self.existdb

    @property
    def exist(self):
        # Cache the "True" response
        if self._exist():
            return True

        # do a head request to check if the file exists.
        # if the file exist (200) then write to cache db
        r = requests.head(self.url(ext=''))
        self.ok = r.ok
        if r.ok:
            self._cache_exist()
        return r.ok


    def upload(self):
        r = requests.post(vimimg, files=dict(name=self.content))
        assert r.ok, 'Upload failed.'

        self.ok = True
        self._cache_exist()
        return r

    def __repr__(self):
        return self.url()
    def __str__(self):
        return self.__repr__()
