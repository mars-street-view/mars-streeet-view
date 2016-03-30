"""Make a live API call and populate the database from the results."""
import os
from sqlalchemy import create_engine
from mars_street_view.api_call import get_one_sol, load_full_sample_data
from mars_street_view.models import DBSession, Base, Photo
import transaction


def populate_one_sol(rover, sol, fetch):
    """Initialize database, query API and write models to database."""
    results = get_one_sol(rover, sol, fetch)
    populate_from_data(results)


def populate_sample_data():
    """Put all photos from sample json data into database."""
    results = load_full_sample_data()
    populate_from_data(results)


def populate_from_data(results):
    """Push the given list of photo dictionaries into the database."""
    photo_list = [Photo(**result) for result in results]
    database_url = os.environ.get("MARS_DATABASE_URL", None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        DBSession.add_all(photo_list)
        DBSession.flush()
