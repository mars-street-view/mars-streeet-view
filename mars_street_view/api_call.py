# _*_ Coding: utf-8 _*_
"""Call the NASA Mars Rover Photo API and return image data."""
from __future__ import unicode_literals

import os
import io
import requests
import json
# from sys import argv


PARENT_DIR = os.path.dirname(__file__)
SAMPLE_DATA_PATH = os.path.join(PARENT_DIR, 'tests', 'sample_data.json')


ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def fetch_photo_data(url, rover, sol):
    """Make API call to NASA."""
    page = 0
    lst = []
    found_ids = set()
    while True:
        params = {
            'sol': sol,
            'page': page,
            'api_key': NASA_API_KEY,
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()  # <- This is a no-op if there is no HTTP error
        content, encoding = resp.content, resp.encoding
        photo_data = json.loads(content.decode(encoding))
        photos = photo_data['photos']
        if not photos:
            break
        for photo in photos:
            if photo['id'] not in found_ids:
                lst.append(photo)
                found_ids.add(photo['id'])
        page += 1

    return lst


def fetch_data_sample():
    """Download and save json data sample of the first day of each mission."""
    photo_list = []
    for rover in ('Spirit', 'Curiosity', 'Opportunity'):
        photo_list.extend(get_one_sol(rover, 1, True))
    data = {'photos': photo_list}
    write_to_json_file(data, SAMPLE_DATA_PATH)


def load_photo_data(rover, sol):
    """Load list of related photos from sample json file instead."""
    data = read_json_from_file(SAMPLE_DATA_PATH)
    return [photo for photo in data['photos']
            if photo['rover']['name'] == rover and photo['sol'] == sol]


def load_full_sample_data():
    """Load list of related photos from sample json file instead."""
    data = read_json_from_file(SAMPLE_DATA_PATH)
    return data['photos']


def write_to_json_file(data, file_name, encoding='utf-8'):
    """Save JSON to a file."""
    with io.open(file_name, encoding=encoding, mode='w') as file:
        json.dump(data, file)


def read_json_from_file(file_name, encoding='utf-8'):
    """Parse JSON."""
    with io.open(file_name, encoding=encoding, mode='r') as file:
        return json.load(file)


def get_one_sol(rover, sol, fetch=False):
    """Return all photos for one sol, given rover and sol."""
    try:
        url = ROVERS[rover]
    except KeyError:
        raise ValueError('Incorrect rover name provided.')
    if fetch:
        photo_list = fetch_photo_data(url, rover, sol)
    else:
        photo_list = load_photo_data(rover, sol)
    return photo_list


if __name__ == '__main__':
    fetch_data_sample()
