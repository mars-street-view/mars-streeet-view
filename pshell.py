"""Run Pyramid Shell from command line interface."""
from webtest import TestApp


def setup(env):
    """Set up the environment for webtests."""
    env['request'].host = 'www.example.com'
    env['request'].scheme = 'https'
    env['testapp'] = TestApp(env['app'])
