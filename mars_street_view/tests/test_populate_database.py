"""Test functions in populate_database.py."""
from mars_street_view.models import DBSession, Photo, Rover, Camera


def test_main(dbtransaction, config_uri, rover_name):
    """Test that main function populates database."""
    from mars_street_view.populate_database import main
    main(rover_name, 1, False, config_uri)
    assert DBSession.query(Photo).count() > 0


def test_populate_sample_data_photos(dbtransaction, config_uri):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.populate_database import populate_sample_data
    from mars_street_view.api_call import load_full_sample_data
    sample_data = load_full_sample_data()
    populate_sample_data(['', config_uri])
    assert DBSession.query(Photo).count() == len(sample_data)


def test_populate_sample_data_rovers(dbtransaction, config_uri):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.populate_database import populate_sample_data
    populate_sample_data(['', config_uri])
    assert DBSession.query(Rover).count() == 3


def test_populate_sample_data_cameras(dbtransaction, config_uri):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.populate_database import populate_sample_data
    populate_sample_data(['', config_uri])
    assert DBSession.query(Camera).count() > 10


def test_populated_rel_photo_rover(dbtransaction, config_uri):
    from mars_street_view.populate_database import populate_sample_data
    populate_sample_data(['', config_uri])
    for photo in DBSession.query(Photo).all():
        assert photo.rover_id is not None
    for rover in DBSession.query(Rover).all():
        # import pdb; pdb.set_trace()
        assert rover.photos.count() > 1


def test_populated_rel_photo_camera(dbtransaction, config_uri):
    from mars_street_view.populate_database import populate_sample_data
    populate_sample_data(['', config_uri])
    for photo in DBSession.query(Photo).all():
        assert photo.rover_id is not None
    for camera in DBSession.query(Camera).all():
        assert camera.photos.count() > 1


# def test_populate_photos_from_fetch(dbtransaction):
#     """Test that photos from each rover populate."""
#     from mars_street_view.api_call import get_one_sol
#     test_list = get_one_sol('Opportunity', 1, fetch=True)
#     new_photos = [Photo(**obj) for obj in test_list]
#     DBSession.add_all(new_photos)
#     DBSession.flush()
#     assert DBSession.query(Photo).count() == len(test_list)
