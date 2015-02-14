import urllib2

from .helpers import is_iso_date, parse_date, load_file


class ApiModel(object):
#    def __init__(self, data):
#        self.id   = data.get('id')
#        self.name = data.get('name')
#        
    def _from_dict(self, data):
        for k,v in data.iteritems():
            if type(v) not in [list, dict]:
                self.__dict__[k] = self._parse_value(v)
       
    def _parse_value(self, value):
        if type(value) in [str, unicode]:
            if is_iso_date(value):
                return parse_date(value)
            else:
                return value
        else:
            return value
        
    def _from_dict_prefixed(self, data, prefix):
        for k,v in data.iteritems():
            if k.startswith(prefix):
                self.__dict__[k.replace(prefix, '')] = v
    
class Tag(ApiModel):
    def __init__(self, id, name, datasets=None):
        self.id = id
        self.name = name
        
        if datasets:
            self.datasets = [Dataset(d) for d in datasets]
    
class Resource(ApiModel):
    def __init__(self, name, data):
        self.name = name
        self.description = data.get('description')
        self.timestamp = parse_date(data.get('revision_timestamp'))
        self._formats = {}
        self._cache = {}
        
    def _add_format(self, info):
        self._formats[info['format'].lower()] = dict(
            id=info.get('id'),
            url=info.get('url'),
            created=parse_date(info.get('created')),
            mimetype=info.get('mimetype'))
        
    @property
    def format_list(self):
        return self._formats.keys()
        
    def get_format(self, name):
        return self._formats.get(name)
        
    def load(self, format_name, use_cache=True):
        if format_name in self._cache and use_cache:
            return self._cache[format_name]
        f = self._formats.get(format_name)
        
        if f:
            return load_file(f['url'], format_name)
        else:
            return None
        
class Dataset(ApiModel):
    def __init__(self, data):
        #super(Dataset, self).__init__(data)
        self._from_dict(data)
        
        self._load_resources(data)
        self._load_tags(data)
        self._load_extras(data)
 
    def _load_resources(self, data):
        self._resources = {}
        for res in data.get('resources', []):
            rid = res['name']
            if rid not in self._resources:
                self._resources[rid] = Resource(rid, data)
            self._resources[rid]._add_format(res)
            
    def _load_tags(self, data):
        self._tags = {}
        for tag in data.get('tags', []):
            self._tags[tag['name']] = Tag(tag['id'], tag['name'])
            
    def _load_extras(self, data):
        self._extras = {}
        for e in data.get('extras', []):
            self._extras[e['key']] = e['value']
        
    @property    
    def resources(self):
        return self._resources.values()
        
    @property    
    def tags(self):
        return self._tags.values()
        
    @property    
    def extras(self):
        return self._extras
