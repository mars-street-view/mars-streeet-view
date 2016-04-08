"""Make a live API call and populate the database from the results."""
import os
from sqlalchemy import create_engine
from mars_street_view.api_call import get_one_sol, load_full_sample_data
from mars_street_view.models import (
    DBSession,
    Base,
    Photo,
    init_rovers_and_cameras
)
import transaction


def populate_one_sol(rover, sol, fetch):
    """Initialize database, query API and write models to database."""
    results = get_one_sol(rover, sol, fetch)
    photo_list = [Photo(**result) for result in results]
    populate_from_data(photo_list)


def populate_sample_data():
    """Put all photos from sample json data into database."""
    results = load_full_sample_data()
    photo_list = [Photo(**result) for result in results]
    populate_from_data(photo_list)


def populate_rovers_cameras():
    """Put all photos from sample json data into database."""
    objects = init_rovers_and_cameras()
    populate_from_data(objects)


def populate_from_data(objects):
    """Push the given list of photo dictionaries into the database."""
    database_url = os.environ.get("MARS_DATABASE_URL", None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        DBSession.add_all(objects)
        DBSession.flush()
