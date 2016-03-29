"""Test that model instances and relationships are created to database."""
from mars_street_view.models import DBSession, Rover, Photo, Camera


def test_rover_db_is_empty(dbtransaction, model_name):
    """Test that the database is empty of each model at test session start."""
    model = globals()[model_name]
    query = DBSession.query(model)
    assert query.count() == 0


def test_db_add(dbtransaction, model_test_params):
    model_name, params = model_test_params
    model = globals()[model_name]
    instance = model(**params)
    DBSession.add(instance)
    DBSession.flush()
    assert DBSession.query(model).count() == 1


def test_photo_rover_relationship(dbtransaction, rover_params, photo_params):
    rover = Rover(**rover_params)
    rover_id = rover.id
    photo_params['rover_id'] = rover_id
    photo = Photo(**photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover_id == rover_id == rover.id


def test_photo_rover_details(dbtransaction, rover_params, photo_params):
    rover = Rover(**rover_params)
    rover_id = rover.id
    rover_landing_date = rover.landing_date
    photo_params['rover_id'] = rover_id
    photo = Photo(**photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover.landing_date == rover_landing_date


def test_photo_camera_relationship(dbtransaction, camera_params, photo_params):
    camera = Camera(**camera_params)
    camera_id = camera.id
    photo_params['camera_id'] = camera.id
    photo = Photo(**photo_params)
    DBSession.add_all([photo, camera])
    DBSession.flush()
    assert photo.camera_id == camera_id == camera.id


def test_full_params(dbtransaction, full_photo_params):
    rover_id = full_photo_params['rover']['id']
    camera_id = full_photo_params['camera']['id']
    photo = Photo(**full_photo_params)
    DBSession.add(photo)
    DBSession.flush()
    assert photo.rover_id == rover_id and photo.camera_id == camera_id


# def test_prepopulated(pre_pop_transaction):
#     assert all([True
#         ])
