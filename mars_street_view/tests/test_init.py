"""Test SQLAlchemy database and Pyramid app initialization."""
import os
from mars_street_view.models import DBSession, Rover, Camera, Photo


def test_db_url(global_environ):
    """Test that tests are correctly using the test datbase."""
    from conftest import TEST_DATABASE_URL
    assert os.environ['MARS_DATABASE_URL'] == TEST_DATABASE_URL


def test_test_app(app):
    """Test that app fixture initializes correctly."""
    from webtest import TestApp
    assert isinstance(app, TestApp)


def test_db_empty(dbtransaction, global_environ):
    """Check that test database initializes empty each time."""
    assert all([DBSession.query(Rover).count() == 0,
                DBSession.query(Camera).count() == 0,
                DBSession.query(Photo).count() == 0])


def test_initialize_db(dbtransaction, config_uri, global_environ):
    """Test that initialize_db runs and populates Rovers and cameras."""
    from mars_street_view.scripts.initializedb import main
    main(['initialize_db', config_uri])
    assert DBSession.query(Rover).count() == 3
    assert DBSession.query(Camera).count() == 19


def test_init_rov_cam(dbtransaction, global_environ):
    """Test that initialize_db runs and populates Rovers and cameras."""
    from mars_street_view.models import init_rovers_and_cameras
    object_list = init_rovers_and_cameras()
    DBSession.add_all(object_list)
    DBSession.flush()
    assert DBSession.query(Rover).count() == 3
    assert DBSession.query(Camera).count() == 19
