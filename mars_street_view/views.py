"""Establish view functions for Mars Street View web app."""
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    Rover,
    Camera,
    Photo
)


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    """Home page view."""
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'mars-street-view'}


class DummyPhoto(object):
    url = "http://funnypics.com/my/cat"
    id = 7

    def __json__(self, request):
        return {'url': self.url}

@view_config(route_name='rover', renderer='json')
def rover_view(request):
    """Return appropriate pictures for a rover request."""
    # import pdb; pdb.set_trace()
    # rover = DBSession.query(Rover).filter_by(name=request.matchdict['rover_name'].capitalize())
    # camera = rover.cameras.filter(name='NAVCAM').one()
    # photo = DBSession.query(Photo).filter_by(camera_id=camera.id)
    # sol = int(request.matchdict['sol'])
    # nav = rover.cameras.filter(name='NAVCAM')
    # nav_today = nav.photos.filter(sol=sol)
    # nav_photo_list = []
    # for photo in nav_today:
    #     nav_photo_list.append(photo)
    nav_photo_list = [DummyPhoto() for i in range(10)]
    return nav_photo_list



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
