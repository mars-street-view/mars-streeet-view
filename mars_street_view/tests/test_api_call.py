# _*_ coding utf-8 _*_
"""Test the api calls."""
import os
import pytest
from mars_street_view.api_call import get_one_sol
from mars_street_view.models import DBSession, Rover, Photo, Camera


# def test_get_inspection_page():
#     """Test that the url returns content."""
#     from api_call import get_inspection_page
#     content, encoding = get_inspection_page('curiosity', 522)
#     print(type(content))

#     assert isinstance(content, bytes)


def test_read_json():
    """Test that our 'read_json' function reads file successfully."""
    from mars_street_view.api_call import read_json
    data = read_json(os.path.join('.', 'sample_data.json'))
    assert isinstance(data, list)
    assert data[0]['id'] == 103389


def test_api_photo_not_dupe(dbtransaction, rover_name):
    test_list = get_one_sol(rover_name, 1)
    photo_ids = [item['id'] for item in test_list]
    print(photo_ids)
    for photo_id in photo_ids:
        assert photo_ids.count(photo_id) == 1
