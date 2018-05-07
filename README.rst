Image / Music uploader
======================

It is a simple (but more complicated than the official one) command line uploader for https://img.vim-cn.com. It is mainly used for my convenience to upload music files and upload as a playlist.

Once installed, running it is also simple::

  img [file] [file...]

Music mode::

  img -m [music] [music...]

For a music playlist, the output format is `hexo-tag-aplayer <https://github.com/MoePlayer/hexo-tag-aplayer>`_ json.


Full Help:
----------

::

  usage: img [-h] [-m] [-p] [-f] FILE [FILE ...]

  Upload file or music to https://img.vim-cn.com/

  positional arguments:
    FILE         a list of files to upload

  optional arguments:
    -h, --help   show this help message and exit
    -m, --music  Use music mode
    -p, --copy   Copy to clipboard
    -f, --force  Force upload
