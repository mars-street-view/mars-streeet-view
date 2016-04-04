"""Test that model instances and relationships are created to database."""
from mars_street_view.models import DBSession, Rover, Photo, Camera


def test_pre_populate_sample_data_photos(pre_pop_transaction, global_environ):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.api_call import load_full_sample_data
    sample_data = load_full_sample_data()
    assert DBSession.query(Photo).count() == len(sample_data)


def test_populated_rel_photo_rover(pre_pop_transaction, global_environ):
    """Test that Rover-Photo relationships of prepopulated DB are correct."""
    for photo in DBSession.query(Photo).all():
        assert photo.rover_name
    for rover in DBSession.query(Rover).all():
        assert rover.photos.count() > 1


def test_populated_rel_photo_camera(pre_pop_transaction, global_environ):
    """Test that Camera-Photo relationships of prepopulated DB are correct."""
    for photo in DBSession.query(Photo).all():
        assert photo.camera_name


def test_populated_rel_rover_camera(pre_pop_transaction, global_environ):
    """Test that Rover-Camera relationships of prepopulated DB are correct."""
    for camera in DBSession.query(Camera).all():
        assert camera.rover_name
    for rover in DBSession.query(Rover).all():
        assert rover.cameras.count() > 1


def test_rov_sol_lots(pre_pop_transaction, global_environ, rover_name,
                      sol):
    """Test get_rov_sol returns correct camera names on pre-populated DB."""
    result = Photo.get_rov_sol(rover_name, sol)
    rover = DBSession.query(Rover).filter(Rover.name == rover_name).one()
    cam_name_list = [camera.name for camera in rover.cameras]
    assert sorted(cam_name_list) == sorted(list(
        result['photos_by_cam'].keys()))


def test_rov_sol_photos(pre_pop_transaction, global_environ, rover_name,
                        sol):
    """Check that all contents of data are Photo objects."""
    result = Photo.get_rov_sol(rover_name, sol)
    photo_list = [photo for photos in result['photos_by_cam'].values()
                  for photo in photos]
    assert len(photo_list) > 0 and all([isinstance(photo, Photo)
                                        for photo in photo_list])


def test_left_lens_only(pre_pop_transaction, global_environ, rover_name,
                        sol):
    """Check that get_sol_rov returns no photos from right lens."""
    result = Photo.get_rov_sol(rover_name, sol)
    photo_list = [photo for photos in result['photos_by_cam'].values()
                  for photo in photos]
    assert photo_list and all([photo.img_src[-11] != 'R'
                               for photo in photo_list])


def test_photo_model_json(pre_pop_transaction, global_environ, photo_params,
                          dummy_request):
    """Assert Photo __json__ value can be converted to and from json."""
    import json
    photo = DBSession.query(Photo).first()
    json_string = json.dumps(photo.__json__(dummy_request))
    assert isinstance(json_string, str)
    assert isinstance(json.loads(json_string), dict)
