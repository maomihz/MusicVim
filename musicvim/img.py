from .main import Vimcn
from .song import Song
from .config import existdb, max_size

import argparse
from json import dumps
from os.path import exists, getsize

import pyperclip

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
        description="Upload file or music to https://img.vim-cn.com/"
    )
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='a list of files to upload')
    parser.add_argument('-m', '--music', action='store_true',
                        help='Use music mode')
    parser.add_argument('-p', '--copy', action='store_true',
                        help='Copy to clipboard')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force upload')
    args = parser.parse_args()

    music = []
    for file in args.files:
        assert exists(file), '%s: File does not exist' % file
        assert args.force or getsize(file) < max_size, '%s: File too large, might cause upload error!\nUse --force to override.' % file

        try:
            if args.music:
                s = Song(file)
                v = s.vimcn
            else:
                v = Vimcn(file)
        except NotImplementedError as e:
            print("%s: %s" % (file, e))
            continue
        except IOError as e:
            print("%s: %s" % (file, e))
            continue

        # Upload file if does not exist
        if not v.exist:
            v.upload()

        # Extract music info
        if args.music:
            cover = s.cover
            if not cover.exist:
                cover.upload()
            music.append((s,v,cover))
        else:
            music.append(v.url())

    if args.music:
        output = json_encode(music)
    else:
        output = '\n'.join(music)
    print(output)

    if args.copy:
        pyperclip.copy(output)
