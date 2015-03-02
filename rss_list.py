import re
import csv
import time
import urllib
import itertools
import argparse
import multiprocessing
from multi import worker
from bs4 import BeautifulSoup


if __name__ == '__main__':
    """Multiprocess ArtExIn RSS feed extractor.

    Extracts from a file named "links" and builds a list of urls to rip
    """
    parser = argparse.ArgumentParser(description='Multiprocess script to '
                                     'extract preformatted data')
#   parser.add_argument('link', metavar='RSS-url', help='url to rss feed to '
#                       'parse')
#   parser.add_argument('path', metavar='PATH', help='path to place newly '
#                       'made zipfiles')
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
    a = 0
    jobs = []
    oklog = manager.list()
    faillog = manager.list()

    # This is where filters to find links we want are assigned.
    http = re.compile('^http\:\/\/www')
    failed_urls = open('failed.urls', 'w')
    succeeded_urls = open('succeeded.urls', 'w')

    # Create list of data to spool
    ulist = open('links', 'r')
    urllist = []
    dw_list = []
    aa_list = []
    urllist = [u.strip() for u in ulist.read().split('\n')
               if u.strip() != '']
    for f in urllist:
        content = []
        i += 1
        print('\nTrying URL...')
        print(f)
        doc = BeautifulSoup(urllib.request.urlopen(f), 'xml')
        print(doc.prettify())
        for item in doc.find_all('link'):
            link = item['href']
            print(link)

            # And this is where filters are checked against links
            if http.search(link):
                content.append(link)
#               aa_list.append(link)
        f = open('urls-%s' % i, 'w')
        for url in content:
            f.write(url + '\n')
        f.close()
