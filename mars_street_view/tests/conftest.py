# -*- coding: utf-8 -*-
"""Configure fixtures for unit and functional tests."""
import os
import pytest
# from webob import multidict
from sqlalchemy import create_engine
from pyramid import testing
from mars_street_view.models import DBSession, Base


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'


@pytest.fixture(scope='session')
def global_environ(request):
    """Establish test database url as a fixture for entire session."""
    prior = os.environ.get('MARS_DATABASE_URL', '')
    os.environ['MARS_DATABASE_URL'] = TEST_DATABASE_URL

    def revert():
        os.environ['MARS_DATABASE_URL'] = prior

    request.addfinalizer(revert)
    return True


@pytest.fixture(scope='session')
def config_uri():
    """Establish configuration uri for initialization."""
    parent_dir = os.path.dirname(__file__)
    gparent_dir = os.path.dirname(parent_dir)
    ggparent_dir = os.path.dirname(gparent_dir)
    return os.path.join(ggparent_dir, 'testing.ini')


@pytest.fixture(scope='session')
def sample_data_uri():
    """Establish configuration uri for initialization."""
    parent_dir = os.path.dirname(__file__)
    return os.path.join(parent_dir, 'sample_data.json')


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


@pytest.fixture()
def pre_pop_transaction(request, sqlengine):
    """Create database transaction connection."""
    from mars_street_view.scripts.initializedb import init_rovers_and_cameras
    from mars_street_view.populate_database import populate_sample_data
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection, expire_on_commit=False)
    init_rovers_and_cameras()
    populate_sample_data()

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(params=['Spirit', 'Curiosity', 'Opportunity'])
def rover_name(request):
    """Establish all rover names to iterate over in tests."""
    return request.param


@pytest.fixture(params=['Photo', 'Rover', 'Camera'])
def model_name(request):
    """Establish all model names to iterate over in tests."""
    return request.param

ROVER_PARAMS = {
    'id': 99,
    'name': "Optimism",
    'landing_date': "2016-03-28",
    'max_sol': 1,
    'max_date': "2016-03-28",
    'total_photos': 9,
}
CAMERA_PARAMS = {
    'id': 29,
    'name': "NAVCAM",
    'rover_name': 'Optimism',
    'full_name': "Navigation Camera"
}
PHOTO_PARAMS = {
    'id': 99,
    'sol': 1,
    'img_src': "image_source",
    'earth_date': "2016-03-28",
    'rover': ROVER_PARAMS,
    'camera': CAMERA_PARAMS
}
TEST_PARAMS = [
    ('Photo', PHOTO_PARAMS),
    ('Rover', ROVER_PARAMS),
    ('Camera', CAMERA_PARAMS),
]


@pytest.fixture(params=TEST_PARAMS)
def model_test_params(request):
    return request.param


@pytest.fixture(scope='session')
def rover_params():
    return ROVER_PARAMS


@pytest.fixture(scope='session')
def photo_params():
    return PHOTO_PARAMS


@pytest.fixture(scope='session')
def camera_params():
    return CAMERA_PARAMS


@pytest.fixture()
def full_photo_params(photo_params, rover_params, camera_params):
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



@pytest.fixture()
def dummy_request():
    """Make a base generic dummy request to be used."""
    request = testing.DummyRequest()
    config = testing.setUp()
    config.add_route('home', '/')
    config.add_route('rover', '/{rover_name}/{sol}')
    return request


@pytest.fixture()
def dummy_get_request(dummy_request):
    """Make a dummy GET request to test views."""
    dummy_request.method = 'GET'
    dummy_request.matchdict = {'rover_name': 'curiosity', 'sol': 1}
    # dummy_request.POST = multidict.NoVars()
    return dummy_request


# @pytest.fixture()
# def dummy_post_request(request, dummy_request):
#     """Make a dummy POST request to test views."""
#     dummy_request.method = 'POST'
#     dummy_request.POST = multidict.MultiDict([('title', 'TESTadd'),
#                                               ('text', 'TESTadd')])

#     def teardown():
#         DBSession.query(Entry).filter(Entry.title == 'TESTadd').delete()

#     request.addfinalizer(teardown)
#     return dummy_request
