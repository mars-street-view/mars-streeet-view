# _*_ Coding: utf-8 _*_
"""Call the NASA Mars Rover Photo API and return image data."""
from __future__ import unicode_literals

import os
import io
import requests
import json
import webbrowser


PARENT_DIR = os.path.dirname(__file__)
SAMPLE_DATA_PATH = os.path.join(PARENT_DIR, 'tests', 'sample_data.json')


ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


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
            print('400 response for {0} {camera} sol {sol} page={page}'
                  ''.format(rover, **params))
            break
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


def fetch_and_save_data_sample():
    """Download and save json data sample of the first day of each mission."""
    photo_list = []
    for rover in ROVERS:
        photo_list.extend(get_one_sol(rover, 1, True))
    data = {'photos': photo_list}
    write_to_json_file(data, SAMPLE_DATA_PATH)
    print('Successfully saved {} photo objects to {}.'
          ''.format(len(photo_list), SAMPLE_DATA_PATH))


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


def get_one_sol(rover, sol, fetch=False, camera=None):
    """Return all photos for one sol, given rover and sol."""
    if fetch:
        photo_list = fetch_photo_data(rover, sol, camera)
    else:
        photo_list = load_photo_data(rover, sol)
    return photo_list


def webbrowse_photos(rover_name, sol_range, camera):
    for n in sol_range:
        results = fetch_photo_data(rover_name, n, camera)
        id_url_list = [(result['id'], result['img_src']) for result in results]
        id_url_list.sort()
        for photo_id, url in id_url_list:
            print('opening url for id {}'.format(photo_id))
            webbrowser.open_new_tab(url)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 5:
        print('Wrong num of args.')
        sys.exit()
    rover_name, start_sol, sol_range, camera = sys.argv[1:]
    sol_range = range(int(start_sol), int(start_sol) + int(sol_range))
    webbrowse_photos(rover_name, sol_range, camera)
