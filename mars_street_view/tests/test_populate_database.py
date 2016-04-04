# """Test functions in populate_database.py."""
# from mars_street_view.models import DBSession, Photo, Rover, Camera


# def test_db_url(global_environ):
#     """Test that tests are correctly using the test datbase."""
#     import os
#     from conftest import TEST_DATABASE_URL
#     assert os.environ['MARS_DATABASE_URL'] == TEST_DATABASE_URL


# def test_db_empty(dbtransaction, global_environ):
#     """Check that test database initializes empty each time."""
#     assert all([DBSession.query(Rover).count() == 0,
#                 DBSession.query(Camera).count() == 0,
#                 DBSession.query(Photo).count() == 0])


# def test_populate_rov_cam(dbtransaction, global_environ):
#     """Test that populate_rovers_cameras works as expected."""
#     from mars_street_view.populate_database import populate_rovers_cameras
#     populate_rovers_cameras()
#     assert DBSession.query(Rover).count() == 3
#     assert DBSession.query(Camera).count() == 19


# def test_populate_one_sol(dbtransaction, rover_name, global_environ):
#     """Test that main function populates database."""
#     from mars_street_view.populate_database import populate_one_sol
#     populate_one_sol(rover_name, 1, False)
#     assert DBSession.query(Photo).count() > 0


# def test_populate_photos_from_fetch(dbtransaction, global_environ):
#     """Test that photos from each rover populate."""
#     from mars_street_view.populate_database import (
#         populate_one_sol, populate_rovers_cameras)
#     populate_rovers_cameras()
#     populate_one_sol('Curiosity', 0, fetch=True)
#     photo_query = DBSession.query(Photo)
#     assert photo_query.count() > 10
#     assert all([getattr(photo, attr) for photo in photo_query
#                 for attr in ('id', 'earth_date', 'img_src',
#                              'rover_name', 'camera_name')])
