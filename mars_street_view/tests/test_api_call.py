# _*_ coding utf-8 _*_
"""Test the api calls."""


def test_fetch_photo_data():
    """Test that the url returns content for one rover."""
    rover_name = 'Curiosity'
    from mars_street_view.api_call import fetch_photo_data, ROVERS
    data = fetch_photo_data(ROVERS[rover_name], rover_name, 522)
    assert isinstance(data, list)


def test_load_photo_data(sample_data_uri, rover_name):
    """Test that our 'read_json' function reads file successfully."""
    from mars_street_view.api_call import load_photo_data
    data = load_photo_data(rover_name, 1)
    assert isinstance(data, list)


def test_load_full_sample_data():
    """Test that sample data from all rovers can be loaded."""
    from mars_street_view.api_call import load_full_sample_data
    data = load_full_sample_data()
    assert all([isinstance(data, list),
                len(data) > 20])


def test_api_photo_not_dupe(rover_name):
    """Confirm that get_one_sol() is not returning duplicate photo ids."""
    from mars_street_view.api_call import get_one_sol
    photos_list = get_one_sol(rover_name, 1)
    photo_ids = [item['id'] for item in photos_list]
    for photo_id in photo_ids:
        assert photo_ids.count(photo_id) == 1
