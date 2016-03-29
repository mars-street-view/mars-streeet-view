"""Test SQLAlchemy database and Pyramid app initialization."""
import os
from mars_street_view.scripts.initializedb import main
from mars_street_view.models import DBSession, MyModel


def test_db_url(global_environ):
    """Test that tests are correctly using the test datbase."""
    from conftest import TEST_DATABASE_URL
    assert os.environ['MARS_DATABASE_URL'] == TEST_DATABASE_URL


def test_test_app(app):
    """Test that app fixture initializes correctly."""
    from webtest import TestApp
    assert isinstance(app, TestApp)


def test_db_empty(app, dbtransaction, global_environ):
    """Check that test database initializes empty each time."""
    assert DBSession.query(MyModel).count() == 0


def test_main(config_uri, global_environ, dbtransaction):
    """Test that main runs."""
    main(['initialize_db',
          config_uri])
