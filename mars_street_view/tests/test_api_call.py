# _*_ coding utf-8 _*_
"""Test the api calls."""
import os
import pytest

JSON_TEST_FILE = os.path.join(os.path.dirname(__file__), 'jsontest.json')


def test_fetch_photo_data():
    """Test that the url returns content for one rover."""
    from mars_street_view.api_call import fetch_photo_data
    rover_name = 'Curiosity'
    data = fetch_photo_data(rover_name, 1)
    assert isinstance(data, list)


def test_fetch_photo_data_fail():
    """Test that the url returns content for one rover."""
    from mars_street_view.api_call import fetch_photo_data
    rover_name = 'NULL'
    with pytest.raises(ValueError):
        fetch_photo_data(rover_name, 1)


def test_load_photo_data(sample_data_uri, rover_name, sol):
    """Test that our 'read_json' function reads file successfully."""
    from mars_street_view.api_call import load_photo_data
    data = load_photo_data(rover_name, sol)
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)


def test_load_full_sample_data():
    """Test that sample data from all rovers can be loaded."""
    from mars_street_view.api_call import load_full_sample_data
    data = load_full_sample_data()
    assert isinstance(data, list) and len(data) > 4000


def test_api_photo_not_dupe(rover_name, sol):
    """Confirm that get_one_sol() is not returning duplicate photo ids."""
    from mars_street_view.api_call import get_one_sol
    photos_list = get_one_sol(rover_name, sol)
    photo_ids = [item['id'] for item in photos_list]
    assert len(photo_ids) == len(set(photo_ids))


def test_write_read_json():
    """Test that data will be written to and read from a json file."""
    from mars_street_view.api_call import (
        write_to_json_file, read_json_from_file)
    data = {'key1': 'val', 'key2': {'subkey': ['a', 'list']}}
    write_to_json_file(data, JSON_TEST_FILE)
    assert read_json_from_file(JSON_TEST_FILE) == data


def test_fetch_and_save_data_sample():
    """Test that function fetches data directly from API and save to json."""
    from mars_street_view.api_call import (
        fetch_and_save_data_sample, read_json_from_file)
    fetch_and_save_data_sample(JSON_TEST_FILE, ['Curiosity'], range(1))
    data = read_json_from_file(JSON_TEST_FILE)
    photos = data.get('photos', None)
    assert isinstance(photos, list) and len(photos) > 10
