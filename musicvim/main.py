from __future__ import print_function

import requests
from os.path import splitext
from hashlib import sha1

from .config import vimimg, existdb

class Vimcn:
    def __init__(self, file):
        self._ext = ''
        self.existdb = existdb
        # Try the bytes object
        if (hasattr(file, 'decode')):
            self.content = file
            self.hash = sha1(self.content)
        # Try file object
        elif (hasattr(file, 'read')):
            self.content = f.read()
        # Assume to be a file name
        else:
            self.name, self._ext = splitext(file)
            with open(file, 'rb') as f:
                self.content = f.read()

        # Calculate the hash
        self.hash = sha1(self.content)
        self.ok = False

    @property
    def ext(self):
        return self._ext

    @ext.setter
    def ext(self, x):
        self._ext = x

    def url(self, ext=None):
        if not ext:
            ext = self.ext or ''
        digest = self.hash.hexdigest()
        result = vimimg + digest[:2] + "/" + digest[2:] + ext
        return result

    def _cache_exist(self):
        self.ok = True
        self.existdb[self.hash.hexdigest()] = 1

    def _exist(self):
        if self.ok:
            return True
        return self.hash.hexdigest() in self.existdb

    @property
    def exist(self):
        # Cache the "True" response
        if self._exist():
            # print('hit')
            return True

        # do the request and cache the result as necessary
        r = requests.head(self.url(ext=''))
        if r.ok:
            self._cache_exist()
        return r.ok

    def upload(self):
        # POST the file
        for i in range(3):
            r = requests.post(vimimg, files=dict(name=self.content))
            if r.ok:
                self._cache_exist()
                return r
        raise Exception("Error uploading file")

    def __repr__(self):
        return self.url()
    def __str__(self):
        return self.__repr__()
