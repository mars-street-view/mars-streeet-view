"""Make a live API call and populate the database from the results."""
from mars_street_view.scripts import initializedb
from mars_street_view.api_call import get_one_sol, load_full_sample_data
from mars_street_view.models import DBSession, Photo


def main(config_uri, rover, sol, fetch):
    """Initialize database, query API and write models to database."""
    initializedb.main(['initializedb', config_uri])
    results = get_one_sol(rover, sol, fetch)
    new_photos = [Photo(**result) for result in results]
    DBSession.add_all(new_photos)
    DBSession.flush()


def populate_sample_data_photos(config_uri):
    initializedb.main(['initializedb', config_uri])
    results = load_full_sample_data()
    new_photos = [Photo(**result) for result in results]
    DBSession.add_all(new_photos)
    DBSession.flush()


def populate_rovers_cameras():
    pass
