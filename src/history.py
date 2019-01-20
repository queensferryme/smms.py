'''Interface for manipulating local history file'''

import datetime
import json
from fnmatch import fnmatch
from os import path
from pathlib import Path


class History:
    '''
    Interface for manipulating local history file, features including:
    * delete a record
    * insert a record
    * search for matching records
    '''
    def __init__(self):
        self.file = path.join(str(Path.home), '.sm.ms.history')
        if not path.exists(self.file):
            with open(self.file, 'wt') as fout:
                json.dump({}, fout)
        with open(self.file, 'rt') as fin:
            self.history = json.load(fin)

    def delete(self, delete_urls):
        '''delete records whose delete url is in list `delete_urls`'''
        delete_urls = tuple(delete_urls)
        for date, items in self.history.items():
            self.history[date] = [item for item in items if item['delete'] not in delete_urls]
        with open(self.file, 'wt') as fout:
            json.dump(self.history, fout, indent=2)

    def filter(self, filenames, comment, dates):
        '''filter matched records & return as a generator'''
        def fnmatches(name, patterns):
            '''extend `fnmatch` to match multiple patterns'''
            for pattern in patterns:
                if fnmatch(name, pattern):
                    return True
            return False
        comment = comment or '*'
        for date in self.history:
            if (not dates) or (date in dates):
                for item in self.history[date]:
                    if fnmatches(item['filename'], filenames) and fnmatch(item['comment'], comment):
                        yield item

    def insert(self, data):
        '''insert a record into history'''
        date = datetime.date.today().isoformat()
        self.history.setdefault(date, []).append(data)
        with open(self.file, 'wt') as fout:
            json.dump(self.history, fout, indent=2)

    def migrate(self):
        '''migrate local history from version 0.0.2 to 1.0.0'''
        for date in self.history:
            for record in self.history[date]:
                if record['comment'] == '--- NO COMMENT ---':
                    record['comment'] = ''
        with open(self.file, 'wt') as fout:
            json.dump(self.history, fout, indent=2)
