"""Make a live API call and populate the database from the results."""
import sys
from mars_street_view.scripts import initializedb
from mars_street_view.api_call import get_one_sol, load_full_sample_data
from mars_street_view.models import DBSession, Photo, Rover, Camera


def main(config_uri, rover, sol, fetch):
    """Initialize database, query API and write models to database."""
    initializedb.main(['initializedb', config_uri])
    results = get_one_sol(rover, sol, fetch)
    new_photos = [Photo(**result) for result in results]
    DBSession.add_all(new_photos)
    DBSession.flush()


def populate_sample_data(argv=sys.argv):
    """Put all photos from sample json data into database."""
    if len(argv) < 2:
        print('Specify a config .ini file.')
        sys.exit()
    config_uri = argv[1]
    initializedb.main(['initializedb', config_uri])
    results = load_full_sample_data()
    obj_list = []
    for obj_name in ('rover', 'camera'):
        found_ids = set()
        for result in results:
            obj = result[obj_name]
            obj_id = obj['id']
            if obj_id not in found_ids:
                found_ids.add(obj_id)
                model = globals()[obj_name.capitalize()]
                obj_list.append(model(**obj))

    obj_list.extend([Photo(**result) for result in results])

    DBSession.add_all(obj_list)
    DBSession.flush()
