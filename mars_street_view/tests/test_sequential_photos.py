"""Tests to see if we can order our photos sequentially."""
import time
import random
import webbrowser
from mars_street_view.models import DBSession, Photo


# def test_in_browser(pre_pop_transaction, global_environ):
#     from mars_street_view.models import Photo
#     rover = random.choice(['Curiosity', 'Opportunity', 'Spirit'])
#     sol = random.choice(range(1, 5))
#     data = Photo.get_rov_sol(rover, sol)
#     cam = random.choice(list(data['photos_by_cam'].keys()))
#     photos = data['photos_by_cam'][cam]
#     for photo in photos:
#         webbrowser.open_new_tab(photo.img_src)
#         time.sleep(1)


def test_photos_sorted(pre_pop_transaction, global_environ):
    rover = random.choice(['Curiosity', 'Opportunity', 'Spirit'])
    sol = random.choice(range(1, 5))
    data = Photo.get_rov_sol(rover, sol)
    cam = random.choice(list(data['photos_by_cam'].keys()))
    photos = data['photos_by_cam'][cam]
    urls_from_method = [photo.img_src for photo in photos]
    query = DBSession.query(Photo, Photo.img_src).filter_by(rover=rover, sol=sol)
    urls_from_query = sorted([photo for photo, in query.all()])
    assert urls_from_method == urls_from_query
