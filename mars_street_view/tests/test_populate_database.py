"""Test functions in populate_database.py."""
from mars_street_view.models import DBSession, Photo


def test_api_photo_populates(dbtransaction, rover_name):
    """Test that photos from each rover populate."""
    from mars_street_view.api_call import get_one_sol
    test_list = get_one_sol(rover_name, 1)
    new_photos = [Photo(**obj) for obj in test_list]
    DBSession.add_all(new_photos)
    DBSession.flush()
    assert DBSession.query(Photo).count() == len(test_list)


def test_main(dbtransaction, config_uri, rover_name):
    """Test that main function populates database."""
    from mars_street_view.populate_database import main
    main(config_uri, rover_name, 1)
    assert DBSession.query(Photo).count() > 0
