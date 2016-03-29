# _*_ Coding: utf-8 _*_
"""Call the NASA Mars Rover Photo API and return image data."""
from __future__ import unicode_literals

import os
import io
import requests
import json
# from sys import argv

ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def get_inspection_page(rover, sol, page):
    """Make API call to NASA."""
    try:
        url = ROVERS[rover]
    except KeyError:
        raise ValueError('Incorrect rover name provided.')

    params = {
        'sol': sol,
        'page': page,
        'api_key': NASA_API_KEY,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()  # <- This is a no-op if there is no HTTP error
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
    lst = []
    found_ids = set()
    while True:
        new_content, encoding = get_inspection_page(rover, sol, page)
        new_content = new_content.decode(encoding)
        photos = json.loads(new_content)['photos']
        if not photos:
            break
        for photo in photos:
            if photo['id'] not in found_ids:
                lst.append(photo)
                found_ids.add(photo['id'])
        page += 1

    # print(lst[-1])
    # print('length of list:')
    # print(len(lst))
    return lst


if __name__ == '__main__':
    # write_to_file(get_inspection_page('curiostiy', 1000, 1), 'sample_data.json')
    # read_json('sample_data.json')
    get_one_sol('curiosity', 780)
