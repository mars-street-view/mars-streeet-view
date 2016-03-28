from mars_street_view.models import DBSession, Rover, Photo


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
