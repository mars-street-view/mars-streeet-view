"""Test that model instances and relationships are created to database."""
from mars_street_view.models import DBSession, Rover, Photo, Camera


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

