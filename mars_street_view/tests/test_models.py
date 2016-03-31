"""Test that model instances and relationships are created to database."""
from mars_street_view.models import DBSession, Rover, Photo, Camera
from mars_street_view.api_call import get_one_sol


def test_db_is_empty(dbtransaction, model_name):
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
    photo_params['rover_name'] = rover.name
    photo = Photo(**photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover_name == rover.name


def test_photo_rover_details(dbtransaction, rover_params, photo_params):
    rover = Rover(**rover_params)
    photo_params['rover_name'] = rover.name
    photo = Photo(**photo_params)
    DBSession.add_all([photo, rover])
    DBSession.flush()
    assert photo.rover.landing_date == rover.landing_date


def test_photo_camera_relationship(dbtransaction, camera_params, photo_params):
    camera = Camera(**camera_params)
    photo_params['camera_name'] = camera.name
    photo = Photo(**photo_params)
    DBSession.add_all([photo, camera])
    DBSession.flush()
    assert photo.camera_name == camera.name


def test_full_params(dbtransaction, full_photo_params):
    rover_name = full_photo_params['rover']['name']
    cam_short_name = full_photo_params['camera']['name']
    camera_name = '_'.join((rover_name, cam_short_name))
    photo = Photo(**full_photo_params)
    DBSession.add(photo)
    DBSession.flush()
    assert photo.rover_name == rover_name and photo.camera_name == camera_name


<<<<<<< HEAD
def test_rov_sol_empty(dbtransaction, global_environ, rover_params):
    rover = rover_params['name']
    sol = 1
    DBSession.add(Rover(**rover_params))
    DBSession.flush()
    assert Photo.get_rov_sol(rover, sol)  == {'rover': rover, 'sol': sol, 'photos_by_cam': {}}


def test_rov_sol_one_camera(dbtransaction, global_environ, rover_params, camera_params):
    rover = rover_params['name']
    camera = '_'.join((rover, camera_params['name']))
    sol = 1
    DBSession.add(Rover(**rover_params))
    DBSession.add(Camera(**camera_params))
    DBSession.flush()
    assert Photo.get_rov_sol(rover, sol) == {'rover': rover, 'sol': sol, 'photos_by_cam': {camera : []}}


def test_rov_sol_one_photo(dbtransaction, global_environ, rover_params, camera_params, photo_params):
    rover = rover_params['name']
    camera = '_'.join((rover, camera_params['name']))
    photo = Photo(**photo_params)
    sol = 1
    DBSession.add(Rover(**rover_params))
    DBSession.add(Camera(**camera_params))
    DBSession.add(photo)
    DBSession.flush()
    assert Photo.get_rov_sol(rover, sol) == {'rover': rover, 'sol': sol, 'photos_by_cam': {camera : [photo]}}


def test_rov_sol_lots(dbtransaction, global_environ, rover_params):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    init_rovers_and_cameras()
    populate_sample_data()
    sol = 1
    result = Photo.get_rov_sol('Curiosity', sol)
    rover = DBSession.query(Rover).filter(Rover.name == 'Curiosity').one()
    cam_name_list = [camera.name for camera in rover.cameras]
    assert sorted(cam_name_list) == sorted(list(result['photos_by_cam'].keys()))


def test_rov_sol_returns_photos(dbtransaction, global_environ):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    init_rovers_and_cameras()
    populate_sample_data()
    sol = 1
    result = Photo.get_rov_sol('Curiosity', sol)
    rover = DBSession.query(Rover).filter(Rover.name == 'Curiosity').one()
    cam_name_list = [camera.name for camera in rover.cameras]
    photo_list = [photo for photos in result['photos_by_cam'].values() 
                  for photo in photos]
    assert len(photo_list) > 0


def test_rov_sol_returns_spirit_filter(dbtransaction, global_environ):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    init_rovers_and_cameras()
    populate_sample_data()
    sol = 1
    result = Photo.get_rov_sol('Spirit', sol)
    photo_list = [photo for photos in result['photos_by_cam'].values() 
                  for photo in photos]
    assert len(photo_list) > 0
    for photo in photo_list:
        if photo.img_src[-11] == 'R':
            assert False
    assert True



def test_photo_model_json(dbtransaction, photo_params, dummy_request):
    import json
    photo = Photo(**photo_params)
    DBSession.add(photo)
    DBSession.flush()
<<<<<<< HEAD
    assert photo.camera_id == camera_id == camera.id


def test_api_photo_result(dbtransaction):
    test_list = get_one_sol('curiosity', 1)
    photos = [Photo(**item) for item in test_list]
    DBSession.add_all(photos)
    DBSession.flush()
    db_len = len(DBSession.query())
    assert len(test_list) == db_len
=======
    json_string = json.dumps(photo.__json__(dummy_request))
    assert isinstance(json_string, str)
    assert isinstance(json.loads(json_string), dict)
>>>>>>> development
=======
# def test_prepopulated(pre_pop_transaction):
#     assert all([True
#         ])
>>>>>>> 06182f80812ccd62ef57a49f4482d7a426d6b8ff
