import re
import csv
import time
import urllib
import argparse
import multiprocessing
from multi import worker
from bs4 import BeautifulSoup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multiprocess script to '
                                     'extract preformatted data')
    parser.add_argument('link', metavar='RSS-url', help='url to rss feed to '
                        'parse')
    parser.add_argument('path', metavar='PATH', help='path to place newly '
                        'made zipfiles')
    parser.add_argument('--edit', metavar='PROCESS', help='script to run on each'
                        'file before zipping it', default=None)
    parser.add_argument('--thumb', metavar='THUMBNAIL', help='link to image to'
                        ' use as a default thumbnail if the page has no'
                        'images', default=None)
    parser.add_argument('--extract', dest='extract', action='store_true')
    parser.add_argument('--no-extract', dest='extract', action='store_false')
    parser.set_defaults(extract=True)
    args = parser.parse_args()

    work_start = time.time()

    manager = multiprocessing.Manager()

    i = 0
    jobs = []
    content = []
    oklog = manager.list()
    faillog = manager.list()
    http = re.compile('^http\:\/\/')
    all_africa = re.compile('stories')
    dw = re.compile('^http\:\/\/dw.de\/')
    failed_urls = open('failed.urls', 'w')
    succeeded_urls = open('succeeded.urls', 'w')

    # Create list of data to spool
    print('Trying URL...')
    doc = BeautifulSoup(urllib.request.urlopen(args.link), 'xml')
    print('URL OK, building list...')
    for item in doc.find_all('link'):
        link = item.get_text().strip()
        if dw.search(link):
            content.append(link)
        elif http.search(link) and all_africa.search(link):
            content.append(link)


    # Begin spooling (skips first row which is human readable column
    #                 identifiers)
    for row in content:
        i += 1
        url = row
        thumb = args.thumb or None
        down = ''

        meta = {}
        meta['partner'] = 'Deutsche Welle'
        meta['is_partner'] = 1
        meta['is_sponsored'] = 0
        meta['keep_formatting'] = 0
        meta['archive'] = 'core'
        meta['license'] = ''

        p = multiprocessing.Process(target=worker,
                                    args=(i, oklog, faillog, args.path, url,
                                          thumb, down, args.extract, meta,
                                          args.edit))
        jobs.append(p)
        p.start()

    # Wrap up processes
    for proc in jobs:
        proc.join()

    # Write output
    for i in faillog:
        failed_urls.write(i + '\n')
    for i in oklog:
        succeeded_urls.write(i + '\n')
    done = time.time() - work_start

    # Give some terminal feedback
    if faillog:
        print('There were some errors...\n')
        for i in faillog:
            print(i + '\n')
    print('Finished in %ss' % done)
