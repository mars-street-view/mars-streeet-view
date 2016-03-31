"""Tests to see if we can order our photos sequentially."""
import random
import webbrowser


def test_in_browser(pre_pop_transaction, global_environ):
    from mars_street_view.models import Photo
    rover = random.choice(['Curiosity', 'Opportunity', 'Spirit'])
    sol = random.choice(range(1, 5))
    data = Photo.get_rov_sol(rover, sol)
    cam = random.choice(list(data['photos_by_cam'].keys()))
    photos = data['photos_by_cam'][cam]
    for photo in photos:
        webbrowser.open_new_tab(photo.img_src)
