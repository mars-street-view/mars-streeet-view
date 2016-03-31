# _*_ Coding: utf-8 _*_
import pytest


def test_rover_view(dummy_get_request, pre_pop_transaction):
    from mars_street_view.views import rover_view
    resp = rover_view(dummy_get_request)
    assert isinstance(resp, dict) and resp.get('photos_by_cam', '')
