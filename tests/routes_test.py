import unittest
from webapp import app, routes

# Load configurables for tests
from .test_params import *


class RoutesTests(unittest.TestCase):

    def setUp(self):
        """ setUp is triggered before executing every test by the framework """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()


    def test_route_home_includes_expected_test(self):
        page_data = self.app.get('/')
        expected = 'Find the right osm2pgsql command'
        msg = 'The expected text was not found:  {}.'.format(expected)
        self.assertTrue(expected in str(page_data.data), msg)

    def test_route_build_url_params_returns_str(self):
        actual = routes.build_url_params(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                         osm_pbf_gb=OSM_PBF_GB_US,
                                         append=False,
                                         pbf_filename='not-important')
        expected = 'system_ram_gb=2&osm_pbf_gb=10.4&append=False&pbf_filename=not-important&pgosm_layer_set=run'
        self.assertEqual(expected, actual)

