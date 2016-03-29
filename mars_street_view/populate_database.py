"""Make a live API call and populate the database from the results."""
from mars_street_view.scripts import initializedb
from mars_street_view.api_call import get_one_sol
from mars_street_view.models import DBSession, Photo


def main(config_uri, rover, sol):
    """Initialize database, query API and write models to database."""
    initializedb.main(['initializedb', config_uri])
    results = get_one_sol(rover, sol)
    new_photos = [Photo(**result) for result in results]
    DBSession.add_all(new_photos)
    DBSession.flush()
