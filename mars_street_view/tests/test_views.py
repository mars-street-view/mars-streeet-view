# _*_ Coding: utf-8 _*_

import pytest
def test_rover_view(dummy_get_request, dbtransaction):
    from mars_street_view.views import rover_view
    resp = rover_view(dummy_get_request)
    assert resp.status_code == 200
