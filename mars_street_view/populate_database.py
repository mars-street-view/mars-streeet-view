"""Make a live API call and populate the database from the results."""
import sys
from mars_street_view.scripts import initializedb
from mars_street_view.api_call import get_one_sol, load_full_sample_data
from mars_street_view import models


def main(rover, sol, fetch, config_uri=None):
    """Initialize database, query API and write models to database."""
    if config_uri:
        args = ['initializedb', config_uri]
    else:
        args = []
    initializedb.main(args)
    results = get_one_sol(rover, sol, fetch)
    new_photos = [models.Photo(**result) for result in results]
    models.DBSession.add_all(new_photos)
    models.DBSession.flush()


def populate_sample_data(args=sys.argv):
    """Put all photos from sample json data into database."""
    initializedb.main(args)
    results = load_full_sample_data()
    obj_list = []
    for obj_name in ('rover', 'camera'):
        found_ids = set()
        for result in results:
            obj = result[obj_name]
            obj_id = obj['id']
            if obj_id not in found_ids:
                found_ids.add(obj_id)
                model = getattr(models, obj_name.capitalize())
                obj_list.append(model(**obj))

    obj_list.extend([models.Photo(**result) for result in results])

    models.DBSession.add_all(obj_list)
    models.DBSession.flush()
