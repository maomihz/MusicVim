import mutagen
from .main import Vimcn

class Song:
    def __init__(self, file):
        self.fname = file
        self.file = mutagen.File(file)
        if self.file == None:
            raise NotImplementedError("File error. Not a music file?")

    @property
    def tags(self):
        return self.file.tags

    @property
    def vimcn(self):
        return Vimcn(self.fname)

    @property
    def name(self):
        try:
            return self.tags['\xa9nam'][0]
        except KeyError:
            pass

        return self.tags['TIT2'].text[0]

    @property
    def artist(self):
        try:
            return self.tags['\xa9ART'][0]
        except KeyError:
            pass

        return self.tags['TPE1'].text[0]

    @property
    def cover(self):
        try:
            cover = self.tags.getall("APIC")[0]
            cover_vim = Vimcn(cover.data)
            if cover.mime == 'image/jpeg':
                cover_vim.ext = '.jpg'
            else:
                cover_vim.ext = '.png'
            return cover_vim
        except:
            pass

        cover = self.tags['covr'][0]
        cover_vim = Vimcn(cover)
        if cover.imageformat == cover.FORMAT_PNG:
            cover_vim.ext = '.png'
        else:
            cover_vim.ext = '.jpg'
        return cover_vim
