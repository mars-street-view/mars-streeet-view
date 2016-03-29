"""Initialize database for SQLAlchemy and Pyramid."""
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    Rover,
    Camera
)


def usage(argv):
    """Print message to stdout explaining correct usage syntax."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Initialize database, optionally with settings from config uri."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    if not settings.get('sqlalchemy.url'):
        try:
            settings['sqlalchemy.url'] = os.environ['MARS_DATABASE_URL']
        except KeyError:
            print('Required MARS_DATABASE_URL not set in global os environ.')
            sys.exit()
        try:
            settings['nasa_api_key'] = os.environ['NASA_API_KEY']
        except KeyError:
            print('Required NASA_API_KEY not set in global os environment.')
            sys.exit()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    init_rovers_and_cameras()


CAMERAS = {
    'FHAZ': "Front Hazard Avoidance Camera",
    "NAVCAM": "Navigation Camera",
    "MAST": "Mast Camera",
    "CHEMCAM": "Chemistry and Camera Complex",
    "MAHLI": "Mars Hand Lens Imager",
    "MARDI": "Mars Descent Imager",
    "RHAZ": "Rear Hazard Avoidance Camera",
    "PANCAM": "Panoramic Camera",
    "MINITES": "Miniature Thermal Emission Spectrometer (Mini-TES)",
    "ENTRY": "Entry, Descent, and Landing Camera"
}


ROVERS = [
    {'name': 'Curiosity',
     'landing_date': "2012-08-06",
     'cameras': ['FHAZ', "NAVCAM", "MAST", "CHEMCAM", "MAHLI", "MARDI",
                 "RHAZ"],
     'max_date': "2016-03-28",
     'max_sol': 1295,
     'total_photos': 246346,
     },
    {'name': 'Spirit',
     'landing_date': "2004-01-04",
     'cameras': ['FHAZ', "NAVCAM", "RHAZ", "PANCAM", "MINITES", "ENTRY"],
     'max_date': "2010-03-21",
     'max_sol': 2208,
     'total_photos': 124550,
     },
    {'name': 'Opportunity',
     'landing_date': "2004-01-25",
     'max_date': "2016-03-28",
     'cameras': ['FHAZ', "NAVCAM", "RHAZ", "PANCAM", "MINITES", "ENTRY"],
     'max_sol': 4328,
     'total_photos': 178933,
     }
]


def init_rovers_and_cameras():
    """Create all Rovers and Cameras and save in database."""
    camera_list = []
    rover_list = []
    for rover_dict in ROVERS:
        rover_list.append(Rover(**rover_dict))
        rover_name = rover_dict['name']
        cam_list = rover_dict['cameras']
        for short_name in cam_list:
            cam_name = '_'.join((rover_name, short_name))
            cam_dict = {
                'name': cam_name,
                'rover_name': rover_name,
                'full_name': CAMERAS[short_name]
            }
            camera_list.append(Camera(**cam_dict))
    DBSession.add_all(rover_list)
    DBSession.add_all(camera_list)
    DBSession.flush()
    transaction.commit()
