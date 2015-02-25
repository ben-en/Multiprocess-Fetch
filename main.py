import csv
import time
import argparse
import multiprocessing
from multi import worker


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multiprocess script to '
                                     'extract preformatted data')
    parser.add_argument('csvfile', metavar='FILE', help='path to the csv '
                        'file conaing a list of urls and metadata')
    parser.add_argument('path', metavar='PATH', help='path to place newly '
                        'made zipfiles')
    parser.add_argument('--edit', metavar='PROCESS', help='script to run on each'
                        'file before zipping it', default=None)
    parser.add_argument('--extract', dest='extract', action='store_true')
    parser.add_argument('--no-extract', dest='extract', action='store_false')
    parser.set_defaults(extract=True)
    args = parser.parse_args()

    work_start = time.time()

    manager = multiprocessing.Manager()

    jobs = []
    content = []
    oklog = manager.list()
    faillog = manager.list()
    failed_urls = open('failed.urls', 'w')
    succeeded_urls = open('succeeded.urls', 'w')
    csv_file = csv.reader(open(args.csvfile, 'r'))

    # Create list of data to spool
    for row in csv_file:
        content.append(row)

    # Begin spooling
    print(args.edit)
    for row in (range(1, len(content))):
        url = content[row][0]
        down = content[row][1]
        thumb = content[row][2]

        meta = {}
        meta['partner'] = ''
        meta['is_partner'] = 0
        meta['is_sponsored'] = 0
        meta['keep_formatting'] = 0
        meta['archive'] = content[row][3] or ''
        meta['license'] = content[row][4] or ''

        p = multiprocessing.Process(target=worker,
                                    args=(row, oklog, faillog, args.path, url,
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
