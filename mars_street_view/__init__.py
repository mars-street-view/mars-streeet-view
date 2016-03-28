"""Initialize Mars Street View app and connection to database."""
import os
import sys
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if not settings.get('sqlalchemy.url'):
        try:
            settings['sqlalchemy.url'] = os.environ['MARS_DATABASE_URL']
        except KeyError:
            print('Required MARS_DATABASE_URL not set in global os environ.')
            sys.exit()
        try:
            settings['mars_api_key'] = os.environ['MARS_API_KEY']
        except KeyError:
            print('Required MARS_API_KEY not set in global os environment.')
            sys.exit()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('rover', '/{rover_name}/{sol}')
    config.scan()
    return config.make_wsgi_app()
