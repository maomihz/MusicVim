from .main import Vimcn
from .song import Song

import argparse
from .config import existdb

def main():
    parser = argparse.ArgumentParser(
        description="Upload file to https://img.vim-cn.com/"
    )
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='a list of files to upload')

    args = parser.parse_args()
    for file in args.files:
        try:
            v = Vimcn(file)
        except IOError as e:
            print(file + ": Unable to read file")
            continue

        if not v.exist:
            v.upload()
        print(v.url())
