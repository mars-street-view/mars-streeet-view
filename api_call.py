# _*_ Coding: utf-8 _*_

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
}


def get_inspection_page(rover):
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
    params['sol'] = 522
    resp = requests.get(url, params=params)
    # import pdb; pdb.set_trace()
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
    return parsed


if __name__ == '__main__':
    # write_to_file(get_inspection_page(rover='curiostiy'), 'sample_data.json')
    read_json('sample_data.json')
