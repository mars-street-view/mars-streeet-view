# _*_ Coding: utf-8 _*_
"""Call the NASA Mars Rover Photo API and return image data."""
from __future__ import unicode_literals

import os
import requests
import json
import time


SAMPLE_DATA_PATH = os.environ.get('SAMPLE_DATA_PATH')

BASE_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/'

ROVERS = {
    'Curiosity': ''.join((BASE_URL, 'curiosity/photos')),
    'Opportunity': ''.join((BASE_URL, 'opportunity/photos')),
    'Spirit': ''.join((BASE_URL, 'spirit/photos')),
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def get_one_sol(rover, sol, fetch=False, camera=None):
    """Return all photos for one sol, given rover and sol."""
    if fetch:
        photo_list = fetch_photo_data(rover, sol, camera)
    else:
        photo_list = load_photo_data(rover, sol)
    return photo_list


def fetch_photo_data(rover, sol, camera=None):
    """Make API call to NASA."""
    try:
        url = ROVERS[rover]
    except KeyError:
        raise ValueError('Incorrect rover name provided.')
    page = 1
    lst = []
    found_ids = set()
    while True:
        params = {
            'sol': sol,
            'page': page,
            'api_key': NASA_API_KEY,
        }
        if camera:
            params['camera'] = camera
        resp = requests.get(url, params=params)
        if resp.status_code == 400:
            params['camera'] = camera or ''
            print('400 response for {0} {camera} sol {sol} page={page}'
                  ''.format(rover, **params))
            break
        content, encoding = resp.content, resp.encoding or 'utf-8'
        photo_data = json.loads(content.decode(encoding))
        photos = photo_data.get('photos', [])
        if not photos:
            break
        for photo in photos:
            if photo['id'] not in found_ids:
                lst.append(photo)
                found_ids.add(photo['id'])
        page += 1

    return lst


def sample_nasa():
    """Function to be called by console script entry point."""
    fetch_and_save_data_sample(SAMPLE_DATA_PATH, ROVERS, range(0, 5))


def fetch_and_save_data_sample(file_path, rovers, sol_range):
    """Download and save json data sample for given sols of each mission."""
    photo_list = []
    for rover in rovers:
        for sol in sol_range:
            photo_list.extend(get_one_sol(rover, sol, True))
            time.sleep(0.5)
    data = {'photos': photo_list}
    write_to_json_file(data, file_path)
    print('Successfully saved {} photo objects to {}.'
          ''.format(len(photo_list), file_path))


def load_photo_data(rover, sol):
    """Load list of related photos from sample json file instead."""
    data = read_json_from_file(SAMPLE_DATA_PATH)
    return [photo for photo in data['photos']
            if photo['rover']['name'] == rover and photo['sol'] == sol]


def load_full_sample_data():
    """Load list of related photos from sample json file instead."""
    data = read_json_from_file(SAMPLE_DATA_PATH)
    return data['photos']


def write_to_json_file(data, file_name):
    """Save JSON to a file."""
    with open(file_name, mode='w') as file:
        json.dump(data, file)


def read_json_from_file(file_name):
    """Parse JSON."""
    with open(file_name, mode='r') as file:
        return json.load(file)
