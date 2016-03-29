"""Test functions in populate_database.py"""
from mars_street_view.models import DBSession, Photo


# def test_main(dbtransaction, config_uri, rover_name):
#     """Test that main function populates database."""
#     from mars_street_view.populate_database import main
#     main(config_uri, rover_name_lower, 1)
#     assert DBSession.query(Photo).count() > 0
