"""Tests to see if we can order our photos sequentially."""


def test_photos_seq(pre_pop_transaction, global_environ, rover_name,
                    sol, camera):
    """Test that pre-populated photos will be retrieved in url sorted order."""
    from mars_street_view.models import Photo
    data = Photo.get_rov_sol(rover_name, sol)
    try:
        photos = data['photos_by_cam'][camera]
        urls_from_method = [photo.img_src for photo in photos]
        prev_url = ''
        for url in urls_from_method:
            assert url > prev_url
            prev_url = url
    except KeyError:
        pass


def test_photos_sorted(pre_pop_transaction, global_environ, rover_name,
                       sol, camera):
    """Second test that pre-populated photos will come in sorted order."""
    from mars_street_view.models import Photo

    data = Photo.get_rov_sol(rover_name, sol)

    try:
        photos = data['photos_by_cam'][camera]
        urls_from_method = [photo.img_src for photo in photos]
        assert urls_from_method == list(sorted(urls_from_method))
    except KeyError:
        pass
