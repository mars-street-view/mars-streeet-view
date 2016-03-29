# -*- coding: utf-8 -*-
"""Configure fixtures for unit and functional tests."""
import os
import pytest
# from webob import multidict
from sqlalchemy import create_engine
# from pyramid import testing
from mars_street_view.models import DBSession, Base


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'


@pytest.fixture(scope='session')
def global_environ():
    """Establish test database url as a fixture for entire session."""
    os.environ['MARS_DATABASE_URL'] = TEST_DATABASE_URL
    return True


@pytest.fixture(scope='session')
def config_uri():
    """Establish configuration uri for initialization."""
    parent_dir = os.path.dirname(__file__)
    gparent_dir = os.path.dirname(parent_dir)
    ggparent_dir = os.path.dirname(gparent_dir)
    return os.path.join(ggparent_dir, 'testing.ini')


@pytest.fixture()
def sqlengine(request):
    """Return sql engine."""
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    """Create database transaction connection."""
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection, expire_on_commit=False)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


ROVER_NAMES = ['Spirit', 'Curiosity', 'Opportunity']


@pytest.fixture(params=ROVER_NAMES)
def rover_name(request):
    return request.param


@pytest.fixture()
def test_rover_params():
    test_rover = {
        'id': 99,
        'name': "Optimism",
        'landing_date': "2016-03-28",
        'max_sol': 1,
        'max_date': "2016-03-28",
        'total_photos': 9,
    }
    return test_rover


@pytest.fixture()
def test_camera_params():
    test_camera = {
        'id': 29,
        'name': "NAVCAM",
        'rover_id': 7,
        'full_name': "Navigation Camera"
    }
    return test_camera


@pytest.fixture()
def test_photo_params():
    test_photo = {
        'id': 99,
        'sol': 1,
        'img_src': "image_source",
        'earth_date': "2016-03-28",
    }
    return test_photo


@pytest.fixture()
def full_photo_params():
    full_params = {
        'id': 549762,
        'sol': 1294,
        'camera': {
            'id': 20,
            'name': "FHAZ",
            'rover_id': 5,
            'full_name': "Front Hazard Avoidance Camera"
        },
        'img_src': "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01294/opgs/edr/fcam/FLB_512366594EDR_F0532406FHAZ00323M_.JPG",
        'earth_date': "2016-03-27",
        'rover': {
            'id': 5,
            'name': "Curiosity",
            'landing_date': "2012-08-06",
            'max_sol': 1294,
            'max_date': "2016-03-27",
            'total_photos': 246214,
        }
    }
    return full_params


@pytest.fixture()
def app(request, global_environ, config_uri):
    """Create pretend app fixture of our main app."""
    from mars_street_view import main
    from webtest import TestApp
    from pyramid.paster import get_appsettings
    settings = get_appsettings(config_uri)
    app = main({}, **settings)
    test_app = TestApp(app)

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_app
