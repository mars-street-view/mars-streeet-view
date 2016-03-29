"""Test functions in populate_database.py."""
from mars_street_view.models import DBSession, Photo, Rover, Camera


def test_populate_one_sol(dbtransaction, rover_name, global_environ):
    """Test that main function populates database."""
    from mars_street_view.populate_database import populate_one_sol
    populate_one_sol(rover_name, 1, False)
    assert DBSession.query(Photo).count() > 0


def test_populate_sample_data_photos(dbtransaction, global_environ):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.populate_database import populate_sample_data
    from mars_street_view.api_call import load_full_sample_data
    sample_data = load_full_sample_data()
    populate_sample_data()
    assert DBSession.query(Photo).count() == len(sample_data)


# def test_populated_rel_photo_rover(dbtransaction, global_environ):
#     from mars_street_view.populate_database import populate_sample_data
#     populate_sample_data()
#     for photo in DBSession.query(Photo).all():
#         assert photo.rover_id is not None
#     for rover in DBSession.query(Rover).all():
#         # import pdb; pdb.set_trace()
#         assert len(rover.photos) > 1


# def test_populated_rel_photo_camera(dbtransaction, config_uri):
#     from mars_street_view.populate_database import populate_sample_data
#     populate_sample_data(['', config_uri])
#     for photo in DBSession.query(Photo).all():
#         assert photo.rover_id is not None
#     for camera in DBSession.query(Camera).all():
#         assert len(camera.photos) > 1


# def test_populate_photos_from_fetch(dbtransaction):
#     """Test that photos from each rover populate."""
#     from mars_street_view.api_call import get_one_sol
#     test_list = get_one_sol('Opportunity', 1, fetch=True)
#     new_photos = [Photo(**obj) for obj in test_list]
#     DBSession.add_all(new_photos)
#     DBSession.flush()
#     assert DBSession.query(Photo).count() == len(test_list)
