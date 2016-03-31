"""Test functions in populate_database.py."""
from mars_street_view.models import DBSession, Photo, Rover, Camera


def test_pre_populate_sample_data_photos(pre_pop_transaction, global_environ):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.api_call import load_full_sample_data
    sample_data = load_full_sample_data()
    assert DBSession.query(Photo).count() == len(sample_data)


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


def test_populated_rel_photo_rover(dbtransaction, global_environ):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    init_rovers_and_cameras()
    populate_sample_data()
    for photo in DBSession.query(Photo).all():
        assert photo.rover_name is not None
    for rover in DBSession.query(Rover).all():
        assert rover.photos.count() > 1


def test_populated_rel_photo_camera(dbtransaction, global_environ):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    init_rovers_and_cameras()
    populate_sample_data()
    for photo in DBSession.query(Photo).all():
        assert photo.camera_name is not None


def test_populated_rel_rover_camera(dbtransaction, global_environ):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    init_rovers_and_cameras()
    populate_sample_data()
    for camera in DBSession.query(Camera).all():
        assert camera.rover_name is not None
    for rover in DBSession.query(Rover).all():
        assert rover.cameras.count() > 1


def test_populate_photos_from_fetch(dbtransaction, global_environ):
    """Test that photos from each rover populate."""
    from mars_street_view.populate_database import populate_one_sol
    populate_one_sol('Curiosity', 0, fetch=True)
    photo_query = DBSession.query(Photo)
    assert photo_query.count() > 10
    for photo in photo_query:
        assert photo.id
        assert photo.sol
        assert photo.earth_date
        assert photo.img_src
        assert photo.rover_name
        assert photo.camera_name
