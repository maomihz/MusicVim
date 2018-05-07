import shelve
import atexit
from os.path import expanduser

existdb_path = expanduser('~/.existdb')
existdb = shelve.open(existdb_path)
vimimg = "https://img.vim-cn.com/"
max_size = 5e7

def cleanup():
    existdb.close()

atexit.register(cleanup)
