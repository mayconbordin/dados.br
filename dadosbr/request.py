import json
import urllib2

from os import path
from urllib import urlencode

from .model import Dataset

class DadosBR(object):
    
    def get_dataset(self, id):
        req = APIRequest('package_show', {'id': id})
        result = req.process()
        return Dataset(result)
        
    def find_datasets(self, query, rows=10, start=0):
        req = APIRequest('package_search', dict(q=query, rows=rows, start=start))
        result = req.process()
        
        return [Dataset(r) for r in result['results']]
        
    @property
    def datasets(self):
        req = APIRequest('package_list')
        return req.process()
        
    def get_tag(self, id):
        req = APIRequest('tag_show', {'id': id})
        result = req.process()
        return Tag(result)
        
    @property
    def tags(self):
        req = APIRequest('tag_list')
        return req.process()

class APIError(Exception):
    def __init__(self, error_message, cause=None, status_code=None):
        self.status_code = status_code
        self.cause = cause
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message

class APIRequest(object):
    base_url = 'http://dados.gov.br/api/3/action'
    
    def __init__(self, resource, params=None):
        self.resource = resource
        self.params = params
        
    def _make_url(self):
        if self.params:
            query = '?' + urlencode(self.params)
        else:
            query = ''
        return path.join(self.base_url, self.resource + query)

    def _make_request(self):
        try:
            req = urllib2.urlopen(self._make_url())
            return json.load(req)
        except urllib2.URLError, e:
            raise APIError('Unable to complete request', e)
        except ValueError, e:
            raise APIError('Invalid JSON response received', e)
            
    def _parse_result(self, result):
        if type(result) == list:
            return result
        
        if result['type'] == 'dataset':
            return Dataset(result)
        elif result['type'] == 'tag':
            return Tag(result)
            
    def process(self):
        data = self._make_request()
        
        if not data['success']:
            raise APIError(data['error']['message'])
            
        return data['result']


