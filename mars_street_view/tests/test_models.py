from mars_street_view.models import DBSession, Rover, Photo, Camera
from mars_street_view.api_call import get_one_sol


def test_rover_db_is_empty(dbtransaction):
    query = DBSession.query(Rover)
    assert query.count() == 0


def test_photo_db_is_empty(dbtransaction):
    query = DBSession.query(Photo)
    assert query.count() == 0


def test_rover_db_add(dbtransaction, test_rover_params):
    rover = Rover(**test_rover_params)
    DBSession.add(rover)
    DBSession.flush()
    assert DBSession.query(Rover).count() == 1


def test_photo_db_add(dbtransaction, test_photo_params):
    photo = Photo(**test_photo_params)
    DBSession.add(photo)
    DBSession.flush()
    assert DBSession.query(Photo).count() == 1


def test_photo_rover_relationship(dbtransaction,
                                  test_rover_params,
                                  test_photo_params):
    rover = Rover(**test_rover_params)
    rover_id = rover.id
    test_photo_params['rover_id'] = rover_id
    photo = Photo(**test_photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover_id == rover_id == rover.id


def test_photo_rover_details(dbtransaction,
                             test_rover_params,
                             test_photo_params):
    rover = Rover(**test_rover_params)
    rover_id = rover.id
    rover_landing_date = rover.landing_date
    test_photo_params['rover_id'] = rover_id
    photo = Photo(**test_photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover.landing_date == rover_landing_date


def test_full_params(dbtransaction,
                     full_photo_params):
    rover_id = full_photo_params['rover']['id']
    photo = Photo(**full_photo_params)
    DBSession.add(photo)
    DBSession.flush()
    assert photo.rover_id == rover_id


def test_camera_add(dbtransaction, test_camera_params):
    camera = Camera(**test_camera_params)
    DBSession.add(camera)
    DBSession.flush()
    assert DBSession.query(Camera).count() == 1


def test_photo_camera_relationship(dbtransaction,
                                   test_camera_params,
                                   test_photo_params):
    camera = Camera(**test_camera_params)
    camera_id = camera.id
    test_photo_params['camera_id'] = camera.id
    photo = Photo(**test_photo_params)
    DBSession.add_all([photo, camera])
    DBSession.flush()
    assert photo.camera_id == camera_id == camera.id


def test_api_photo_result(dbtransaction):
    test_list = get_one_sol('curiosity', 1)
    photos = [Photo(**item) for item in test_list]
    DBSession.add_all(photos)
    DBSession.flush()
    db_len = len(DBSession.query())
    assert len(test_list) == db_len
