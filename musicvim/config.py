import shelve
import atexit
from os.path import expanduser

existdb_path = expanduser('~/.existdb')
existdb = shelve.open(existdb_path)
vimimg = "https://img.vim-cn.com/"

def cleanup():
    existdb.close()

atexit.register(cleanup)
