import re
import urllib2
import json
import csv

from StringIO import StringIO
from datetime import datetime

def is_iso_date(date):
    match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', date)
    return match != None


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    
def load_file(url, format_name):
    try:
        r = urllib2.urlopen(url)
        
        if format_name == 'json':
            return json.load(r)
        elif format_name == 'csv':
            csvfile = StringIO(r.read())
            dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,")
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            return [row for row in reader]
        else: # xml, HTML, others
            return None
    except urllib2.URLError, e:
        return None
