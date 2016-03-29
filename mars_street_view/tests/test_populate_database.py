"""Test functions in populate_database.py."""
from mars_street_view.models import DBSession, Photo


def test_main(dbtransaction, config_uri, rover_name):
    """Test that main function populates database."""
    from mars_street_view.populate_database import main
    main(config_uri, rover_name, 1, False)
    assert DBSession.query(Photo).count() > 0


def test_photos_from_sample(dbtransaction, config_uri):
    """Test that sample data can be loaded into DB."""
    from mars_street_view.populate_database import populate_sample_data_photos
    from mars_street_view.api_call import load_full_sample_data
    sample_data = load_full_sample_data()
    populate_sample_data_photos(config_uri)
    assert DBSession.query(Photo).count() == len(sample_data)


def test_populate_photos_from_fetch(dbtransaction):
    """Test that photos from each rover populate."""
    from mars_street_view.api_call import get_one_sol
    test_list = get_one_sol('Opportunity', 1, fetch=True)
    new_photos = [Photo(**obj) for obj in test_list]
    DBSession.add_all(new_photos)
    DBSession.flush()
    assert DBSession.query(Photo).count() == len(test_list)
