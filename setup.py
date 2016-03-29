"""Setup for Mars Street View app."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

REQUIRES = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'psycopg2',
    'requests',
]
TEST = [
    'pytest',
    'pytest-watch',
    'tox',
    'coverage',
    'pytest-cov',
    'webtest'
]

DEV = [
    'ipython',
    'pyramid-ipython',
    'pyramid_debugtoolbar'
]


setup(name='mars-street-view',
      version='0.0',
      description='Web application to explore mars.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author=('Munir Ibrahim, Hannah Krager, Paul Sheridan, '
              'Patrick Trompeter and Will Weatherford'),
      author_email='',
      url='',
      license='MIT',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='mars_street_view',
      install_requires=REQUIRES,
      extras_require={
          'test': TEST,
          'dev': DEV
      },
      entry_points="""\
      [paste.app_factory]
      main = mars_street_view:main
      [console_scripts]
      initialize_db = mars_street_view.scripts.initializedb:main
      sample_nasa = mars_street_view.api_call:fetch_and_save_data_sample
      populate_sample = mars_street_view.populate_database:populate_sample_data
      """,
      )
