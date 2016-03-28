# _*_ Coding: utf-8 _*_
from __future__ import unicode_literals

import os
import io
import requests
import json
# from sys import argv

CURIOSITY = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
OPPORTUNITY = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'
SPIRIT = 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos'
NASA_API = os.environ.get('NASA_API_KEY')

INSPECTION_PARAMS = {
    'sol': "",
    'api_key': NASA_API,
    'page': "",
}


def get_inspection_page(rover, sol, page):
    """Make API call to NASA."""
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
    params['sol'] = sol
    params['page'] = page
    resp = requests.get(url, params=params)
    resp.raise_for_status()  # <- This is a no-op if there is no HTTP error
    # remember, in requests `content` is bytes and `text` is unicode
    return resp.content, resp.encoding


def write_to_file(resp, file_name):
    """Save JSON to a file."""
    content, encoding = resp
    file = io.open(file_name, encoding='utf-8', mode='w')
    file.write(content.decode(encoding))
    file.close()


def read_json(file):
    """Parse JSON."""
    text = io.open(file, encoding='utf-8', mode='r')
    unparsed = text.read()
    parsed = json.loads(unparsed)
    return parsed['photos']


def get_one_sol(rover, sol):
    """Return all photos for one sol, given rover and sol."""
    page = 0
    content, encoding = get_inspection_page(rover, sol, page)
    content = content.decode('utf-8')
    pcontent = json.loads(content)
    lst = list(pcontent['photos'])
    while pcontent['photos'] != []:
        page += 1
        new_content, encoding = get_inspection_page(rover, sol, page)
        new_content = new_content.decode('utf-8')
        pcontent = json.loads(new_content)
        lst.extend(pcontent['photos'])
        # print("test 25: " + str(pcontent))
        # print("******************")
        # print('len: ' + str(len(lst)))
    print(lst[-1])
    print('length of list:')
    print(len(lst))
    return lst



if __name__ == '__main__':
    # write_to_file(get_inspection_page('curiostiy', 1000, 1), 'sample_data.json')
    # read_json('sample_data.json')
    get_one_sol('curiosity', 780)
