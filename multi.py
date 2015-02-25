import re
import time
import shutil
import hashlib
from os.path import join

from fetch import fetch, fetch_file, check_url, zip_up


def hash_url(url):
    md5 = hashlib.md5()
    md5.update(bytes(url, 'utf-8'))
    return md5.hexdigest()


def worker(pid, oklog, faillog, path, url, thumb, down, extract, metadata,
           post):
    '''Process to be run by main.py

    Arguments taken:
        'oklog'    ->  Dictionary to put successful urls into
        'faillog'  ->  List to put failed urls into
        'url'      ->  Link to site to zip [str]
        'path'     ->  Path to create zipfiles in [str]
        'thumb'    ->  Url to thumbnail (if page doesn't have any images) [str]
        'metadata' ->  Dict of metadata to include in zipfile

    Logs start time, checks url, downloads url, checks for extra files,
    downloads them if necessary, and zips everything up.
    '''
    start = time.time()
    http = re.compile('^http')
    md5 = hash_url(url)

    print("[PID:%s] Processing '%s'" % (pid, url))
    if check_url(url, 5):
        meta = fetch(url, path, md5, extract, metadata)
        if http.match(thumb):
            if check_url(thumb):
                fetch_file(thumb, path, md5, 'thumbnail')
            else:
                print("\nThumbnail url check failed!\n%s\n" % thumb)
                faillog.append(thumb)
        if http.match(down):
            if check_url(down):
                down_name = re.search("([^/.]*\.pdf)", down).group(0)[:-4]
                fetch_file(down, path, md5, down_name)
            else:
                print("\nDownload file url check failed!\n%s\n" % down)
                faillog.append(down)
    else:
        faillog.append(url)
        print("\nUrl check failed!\n'%s'\n" % url)
        zip_up(md5, path)
        finished = time.time() - start
        oklog.append(url)
    else:
        faillog.append(url)
        print("\nUrl check failed!\n%s\n" % url)
    shutil.rmtree(join(path, md5))
    print('[PID: %s] Completed successfully in %ss.' % (pid, finished))
        print('[PID: %s] Completed successfully in %ss.' % (pid, finished))
