#!/usr/bin/python3

"""Search all the ISBNs on Douban and create doc files."""

import os
import sys
import time
import json
import urllib.request

UA = 'USTCLUGbot-Library/1.0 (+https://github.com/ustclug/library)'
headers = {'User-Agent': UA}

file_format = '''---
title: {0[title]}
isbn: {0[isbn]}
author: {0[author]}
keywords: {0[keywords]}
source: unknown
available: TRUE
douban_url: {0[douban_url]}
---
'''

def retry(func):
    def wrap(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e, 'retry...')
                time.sleep(60)
    return wrap

@retry
def fetch_douban(isbn):
    url = 'https://api.douban.com/v2/book/isbn/%s' % isbn
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as http:
        data = json.load(http)
    return dict(isbn=isbn,
                title=data['title'],
                author=', '.join(data['author']),
                keywords=', '.join(i['name'] for i in data['tags']),
                douban_url=data['alt'])

if __name__ == '__main__':
    data = []
    for line in sys.stdin:
        data.append(fetch_douban(line.strip()))
        print(data[-1])
    date = time.strftime('%Y-%m-%d')
    number = '%%0%dd' % len(str(len(data) - 1))
    path = os.path.join('..', 'docs', '_posts', date + '-' + number)
    for i in range(len(data)):
        book = data[i]
        with open(path % i, 'w') as f:
            f.write(file_format.format(book))
