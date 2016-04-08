"""Testing that our routes and Pyramid return responses as expected."""
# _*_ Coding: utf-8 _*_


def test_rover_view(dummy_get_request, pre_pop_transaction):
    """Test that rover_view returns an expected dict."""
    from mars_street_view.views import rover_view
    resp = rover_view(dummy_get_request)
    assert isinstance(resp, dict) and resp.get('photos_by_cam', '')


def test_app_index(pre_pop_transaction, app):
    """Test that index view returns OK response through app."""
    response = app.get('/')
    assert response.status_code == 200


def test_app_rover(pre_pop_transaction, app, rover_name, sol):
    """Test that rover view returns OK response through app."""
    response = app.get('/{}/{}'.format(rover_name, sol))
    assert response.status_code == 200
