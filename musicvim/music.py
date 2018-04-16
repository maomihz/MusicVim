from .main import Vimcn
from .song import Song

from json import dumps
import argparse


def json_encode(music):
    result = {
        'music': []
    }
    for song, file, cover in music:
        result['music'].append({
            'title': song.name,
            'artist': song.artist,
            'url': file.url(),
            'pic': cover.url()
        })
    return dumps(result, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Upload music to https://img.vim-cn.com/"
    )
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='a list of music files to upload')

    args = parser.parse_args()
    music = []
    for file in args.files:
        try:
            s = Song(file)
            v = s.vimcn
        except IOError as e:
            print(file + ": Unable to read music file")
            continue

        if not v.exist:
            v.upload()
        cover = s.cover
        if not cover.exist:
            cover.upload()
        music.append((s,v,cover))

    print(json_encode(music))
