# _*_ coding utf-8 _*_
"""Test the api calls."""
import pytest


# def test_get_inspection_page():
#     """Test that the url returns content."""
#     from api_call import get_inspection_page
#     content, encoding = get_inspection_page('curiosity', 522)
#     print(type(content))

#     assert isinstance(content, bytes)


def test_read_json():
    """Test that our 'read_json' function reads file successfully."""
    from api_call import read_json
    data = read_json('sample_data.json')
    assert isinstance(data, list)
    assert data[0]['id'] == 1735

# def test_scrub_data():
#     """Test that our function will return """
