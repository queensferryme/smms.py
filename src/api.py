'''Wrapper for RESTful api https://sm.ms/api'''

import requests


class Api:
    '''Wrapper for RESTful api https://sm.ms/api'''
    params = {'format': 'json', 'ssl': True}
    prefix = 'https://sm.ms/api'

    @classmethod
    def delete(cls, delete_url):
        '''delete an image from remote server'''
        return requests.get(delete_url).ok

    @classmethod
    def upload(cls, image):
        '''upload an image file'''
        files = {'smfile': open(image, 'rb')}
        print()
        resp = requests.post('{}/upload'.format(cls.prefix), files=files, params=cls.params)
        return resp.text
