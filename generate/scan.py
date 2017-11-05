#!/usr/bin/python3

"""Get ISBNs from PocketLibrary's backup files."""

import os
import sys
import sqlite3

if __name__ == '__main__':
    dirs = sys.argv[1:]
    if not dirs:
        dirs = [os.path.join('..', d) for d in os.listdir('..')
                if d.startswith('PocketLibrary')]
    for d in dirs:
        con = sqlite3.connect(os.path.join(d, 'Backup', 'pocketlibrary.db'))
        cur = con.cursor()
        cur.execute('SELECT ISBN FROM books')
        for r in cur.fetchall():
            print(r[0])
        con.close()
