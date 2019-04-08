import requests, json
from advanced_expiry_caching import *

### get the data from the cache file if it exists and is not expired; else, get request the We the People API and cache the response

BASEURL = 'https://api.whitehouse.gov/v1/petitions.json'
CACHE =  Cache('petitions_cache.json')

data = CACHE.get(BASEURL)
if not data:
    params = {'limit':1000}
    resp = requests.get(BASEURL, params).text
    resp_dict = json.loads(resp)
    CACHE.set(BASEURL, resp_dict)
