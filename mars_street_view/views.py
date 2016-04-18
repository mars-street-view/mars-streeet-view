"""Establish view functions for Mars Street View web app."""
from __future__ import unicode_literals, print_function
from pyramid.view import view_config

from .models import Photo


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    """Home page view."""
    return {'project': 'mars-street-view'}


@view_config(route_name='rover', renderer='json')
def rover_view(request):
    """Return appropriate pictures for a rover request."""
    rover = request.matchdict['rover_name']
    sol = int(request.matchdict['sol'])
    data = Photo.get_rov_sol(rover, sol)
    return data
