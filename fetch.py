import os
from os.path import dirname as up, abspath, join
import sys
import time
import urllib

sys.path.insert(0, up(up(abspath(__file__))))
sys.path.insert(0, join(up(up(abspath(__file__))), 'artexin'))

from artexin.pack import collect, zipdir
from artexin.preprocessor_mappings import get_preps

def fetch(url, path, md5, extract, meta):
    '''Fetches url with 'collect()'

    keep_dir is used to bypass collect()'s tendency to create a zipball then
    remove the working directory. We create our own zipball later once we're
    sure we don't need to download any other files or have done so.
    '''

    meta = collect(url, prep=get_preps(url), base_dir=path, meta=meta,
                   keep_dir=True, do_extract=extract)
    os.remove(join(path, '%s.zip' % md5))
    return meta


def fetch_file(url, path, md5, filename):
    '''Fetches a url and places it into the designated folder (path/md5)'''

    ext = url[-3:]
    urllib.request.urlretrieve(url, join(path, md5, '%s.%s' % (filename, ext)))


def check_url(url, retries=1):
    '''Simply checks whether a url is valid or not'''
    for _ in range(retries):
        try:
            urllib.request.urlopen(url)
            return(True)
        except e:
            print('Retrying URL...')
            pass
    else:
        print('Url that failed: "' + url + '"')
        return(False)


def zip_up(md5, path):
    '''zips a specified md5 in a specified directory'''

    zipdir(join(path, '%s.zip' % md5), join(path, md5))
