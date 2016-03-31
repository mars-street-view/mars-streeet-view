"""Test that model instances and relationships are created to database."""
from mars_street_view.models import DBSession, Rover, Photo, Camera


def test_db_is_empty(dbtransaction, model_name):
    """Test that the database is empty of each model at test session start."""
    model = globals()[model_name]
    query = DBSession.query(model)
    assert query.count() == 0


def test_db_add(dbtransaction, model_test_params):
    """Test that one of each type of model can be added to the DB."""
    model_name, params = model_test_params
    model = globals()[model_name]
    instance = model(**params)
    DBSession.add(instance)
    DBSession.flush()
    assert DBSession.query(model).count() == 1


def test_photo_rover_relationship(dbtransaction, rover_params, photo_params):
    """Test Rover, Photo have correct relationship after initialization."""
    rover = Rover(**rover_params)
    photo_params['rover_name'] = rover.name
    photo = Photo(**photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover_name == rover.name


def test_photo_rover_details(dbtransaction, rover_params, photo_params):
    """Test that Photo can access Rover's attributes through relationship."""
    rover = Rover(**rover_params)
    photo_params['rover_name'] = rover.name
    photo = Photo(**photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert all([getattr(rover, attr) == getattr(photo.rover, attr)
                for attr in rover_params])


def test_photo_camera_relationship(dbtransaction, camera_params, photo_params):
    """Test that Photo can access Camera's attributes through relationship."""
    camera = Camera(**camera_params)
    photo_params['camera_name'] = camera.name
    photo = Photo(**photo_params)
    DBSession.add_all([photo, camera])
    DBSession.flush()
    assert all([getattr(camera, attr) == getattr(photo.camera, attr)
                for attr in camera_params])


def test_full_params(dbtransaction, full_photo_params):
    """Test that a full set of params from NASA API will construct models."""
    rover_name = full_photo_params['rover']['name']
    cam_short_name = full_photo_params['camera']['name']
    camera_name = '_'.join((rover_name, cam_short_name))
    photo = Photo(**full_photo_params)
    DBSession.add(photo)
    DBSession.flush()
    assert photo.rover_name == rover_name and photo.camera_name == camera_name


def test_rov_sol_empty(dbtransaction, global_environ, rover_params):
    """Test get_rov_sol return value for Rover with no cameras or photos."""
    rover = rover_params['name']
    sol = 1
    DBSession.add(Rover(**rover_params))
    DBSession.flush()
    expected = {'rover': rover, 'sol': sol, 'photos_by_cam': {}}
    assert Photo.get_rov_sol(rover, sol) == expected


def test_rov_sol_one_camera(dbtransaction, global_environ, rover_params,
                            camera_params):
    """Test get_rov_sol return value for a Rover with one Camera."""
    rover = rover_params['name']
    camera = '_'.join((rover, camera_params['name']))
    sol = 1
    DBSession.add(Rover(**rover_params))
    DBSession.add(Camera(**camera_params))
    DBSession.flush()
    expected = {'rover': rover, 'sol': sol, 'photos_by_cam': {camera: []}}
    assert Photo.get_rov_sol(rover, sol) == expected


def test_rov_sol_one_photo(dbtransaction, global_environ, rover_params,
                           camera_params, photo_params):
    """Test return value for get_rov_sol with one Photo."""
    rover = rover_params['name']
    camera = '_'.join((rover, camera_params['name']))
    photo = Photo(**photo_params)
    sol = 1
    DBSession.add(Rover(**rover_params))
    DBSession.add(Camera(**camera_params))
    DBSession.add(photo)
    DBSession.flush()
    expected = {'rover': rover, 'sol': sol, 'photos_by_cam': {camera: [photo]}}
    assert Photo.get_rov_sol(rover, sol) == expected


def test_rov_sol_lots(pre_pop_transaction, global_environ, rover_name):
    """Test get_rov_sol returns correct camera names on pre-populated DB."""
    sol = 1
    result = Photo.get_rov_sol(rover_name, sol)
    rover = DBSession.query(Rover).filter(Rover.name == rover_name).one()
    cam_name_list = [camera.name for camera in rover.cameras]
    assert sorted(cam_name_list) == sorted(list(
        result['photos_by_cam'].keys()))


def test_rov_sol_gets_photos(pre_pop_transaction, global_environ, rover_name):
    """Check that all contents of data are Photo objects."""
    sol = 1
    result = Photo.get_rov_sol('Curiosity', sol)
    photo_list = [photo for photos in result['photos_by_cam'].values()
                  for photo in photos]
    assert len(photo_list) > 0 and all([isinstance(photo, Photo)
                                        for photo in photo_list])


def test_rov_sol_returns_spirit_filter(pre_pop_transaction, global_environ):
    """Check that get_sol_rov returns no photos from right lens."""
    sol = 1
    result = Photo.get_rov_sol('Spirit', sol)
    photo_list = [photo for photos in result['photos_by_cam'].values()
                  for photo in photos]
    assert len(photo_list) > 0
    for photo in photo_list:
        if photo.img_src[-11] == 'R':
            assert False
    assert True


def test_photo_model_json(dbtransaction, global_environ, photo_params,
                          dummy_request):
    """Assert Photo __json__ value can be converted to and from json."""
    import json
    photo = Photo(**photo_params)
    DBSession.add(photo)
    DBSession.flush()
    json_string = json.dumps(photo.__json__(dummy_request))
    assert isinstance(json_string, str)
    assert isinstance(json.loads(json_string), dict)
