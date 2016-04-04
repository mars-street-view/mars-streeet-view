"""Establish view functions for Mars Street View web app."""
from __future__ import unicode_literals, print_function
from pyramid.view import view_config

from .models import Photo


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    """Home page view."""
    return {'project': 'mars-street-view'}


class DummyPhoto(object):
    """Object for testing an expected Photo object."""

    url = 'http://i.telegraph.co.uk/multimedia/archive/02445/mars_2445397b.jpg'
    id = 7

    def __json__(self, request):
        """Return dict object suitable for converting into json."""
        return {'url': self.url}


@view_config(route_name='rover', renderer='json')
def rover_view(request):
    """Return appropriate pictures for a rover request."""
    rover = request.matchdict['rover_name']
    # Photo.get_rov_sol returns a dictionary with keys 'rov', 'sol',
    # and photos_by_cam
    sol = int(request.matchdict['sol'])
    data = Photo.get_rov_sol(rover, sol)
    return data


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_mars-street-view_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
