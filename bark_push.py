'''
https://github.com/Finb/Bark
'''

import requests
import json

class BarkPush():
    def __init__(self, key, api_server = 'api.day.app'):
        self.key = key
        self.api_server = api_server
    
    def push(self, body, title = 'Bark', url = None, is_archive = None, group = None, icon = None, copy = None, automatically_copy = 0):
        request_url = 'https://{0}/{1}/{2}/{3}'.format(self.api_server, self.key, title, body)
        payload = {}
        if url:
            payload['url'] = url
        if is_archive:
            payload['isArchive'] = is_archive
        if group:
            payload['group'] = group
        if icon:
            payload['icon'] = icon
        if copy:
            payload['copy'] = copy
        if automatically_copy:
            payload['automaticallyCopy'] = automatically_copy
        return json.loads(requests.get(request_url, params = payload).content.decode())

if __name__ == '__main__':
    from secrets import BARK_PUSH_KEY
    key = BARK_PUSH_KEY
    bark = BarkPush(key)
    print(bark.push('This Notification Opens Google', title='Test', url='http://www.google.com', is_archive=1, group='test', icon='http://www.google.com/favicon.ico', copy='COPY!', automatically_copy=1))
