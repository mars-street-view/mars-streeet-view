"""Initialize database for SQLAlchemy and Pyramid."""
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    init_rovers_and_cameras,
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
    # import pdb; pdb.set_trace()
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
    objects_list = init_rovers_and_cameras()
    with transaction.manager:
        DBSession.add_all(objects_list)
        DBSession.flush()
