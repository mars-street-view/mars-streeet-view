"""Tests to see if we can order our photos sequentially."""
import random


def test_photos_seq(pre_pop_transaction, global_environ):
    """Test that pre-populated photos will be retrieved in url sorted order."""
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
    """Second test that pre-populated photos will come in sorted order."""
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
    urls_from_query = sorted([url for photo, url in query.all()
                              if url[-11] != 'R'])
    assert urls_from_method == urls_from_query
