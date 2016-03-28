"""Setup for Mars Street View project."""

from setuptools import setup, find_packages

REQUIRES = [
    'pyramid',
    'pyramid_jinja2',
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
    'webtest']

DEV = [
    'ipython',
    'pyramid-ipython',
    'pyramid_debugtoolbar'
]

setup(name='mars-street-view',
      description='Command line program to manage mars-street-view.',
      version=0.1,
      keywords=[],
      classifiers=[],
      author='Will Weatherford',
      author_email='weatherford.william@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      # py_modules=[],
      # package_dir={'': ''},
      install_requires=[],
      extras_require={'test': TEST,
                      'dev': DEV}
      )
