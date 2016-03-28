# _*_ Coding: utf-8 _*_

import os
import requests
from sys import argv

CURIOSITY = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
OPPORTUNITY = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'
SPIRIT = 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos'
NASA_API = os.environ.get('NASA_API_KEY')

INSPECTION_PARAMS = {
    'sol': "",
    'api_key': NASA_API,
}

def get_inspection_page(rover):
    url = ""
    if rover == 'spirit':
        url = SPIRIT
    elif rover == 'opportunity':
        url = OPPORTUNITY
    else:
        url = CURIOSITY

    params = INSPECTION_PARAMS.copy()
    # for key, val in kwargs.items():
    #     if key in INSPECTION_PARAMS:
    #         params[key] = val
    params['sol'] = 522
    resp = requests.get(url, params=params)
    import pdb; pdb.set_trace()
    resp.raise_for_status() # <- This is a no-op if there is no HTTP error
    # remember, in requests `content` is bytes and `text` is unicode
    return resp.content, resp.encoding

if __name__ == '__main__':
    get_inspection_page(rover='curiostiy')

