"""Tests to see if we can order our photos sequentially."""
import time
import random
import webbrowser


def test_photos_seq(pre_pop_transaction, global_environ):
    from mars_street_view.models import Photo
    rover_name = random.choice(['Curiosity', 'Opportunity', 'Spirit'])
    sol = random.choice(range(1, 5))
    data = Photo.get_rov_sol(rover_name, sol)
    cam = random.choice(list(data['photos_by_cam'].keys()))
    photos = data['photos_by_cam'][cam]
    urls_from_method = [photo.img_src for photo in photos]
    prev_url = ''
    for url in urls_from_method:
        assert url > prev_url
        prev_url = url


def test_photos_sorted(pre_pop_transaction, global_environ):
    from mars_street_view.models import DBSession, Photo
    rover_name = random.choice(['Curiosity', 'Opportunity', 'Spirit'])
    sol = random.choice(range(1, 5))
    data = Photo.get_rov_sol(rover_name, sol)
    cam = random.choice(list(data['photos_by_cam'].keys()))
    photos = data['photos_by_cam'][cam]
    urls_from_method = [photo.img_src for photo in photos]
    query = DBSession.query(
        Photo, Photo.img_src).filter_by(rover_name=rover_name,
                                        camera_name=cam, sol=sol)
    urls_from_query = sorted([url for photo, url in query.all() if url[-11] != 'R'])
    assert urls_from_method == urls_from_query


ROVER = 'Curiosity'
SOL = 330
CAMERA = 'NAVCAM'


def test_in_browser(dbtransaction, global_environ):
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_one_sol
    from mars_street_view.models import Photo
    init_rovers_and_cameras()
    populate_one_sol(ROVER, SOL, fetch=True)
    print('Getting data for {} sol {}'.format(ROVER, SOL))
    data = Photo.get_rov_sol(ROVER, SOL)
    cam_name = '_'.join((ROVER, CAMERA))
    photo_list = data['photos_by_cam'].get(cam_name, [])
    for photo in photo_list:
        trunc_url = photo.img_src.split('/')[-1]
        print('{camera_name} url {0}; id {id} nasa_id {nasa_id}'
              ''.format(trunc_url, **photo.__json__(None)))
        webbrowser.open_new_tab(photo.img_src)
        time.sleep(1)
