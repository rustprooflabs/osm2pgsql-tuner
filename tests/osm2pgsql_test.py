""" Unit tests to cover the pgconfig module."""
import unittest
from webapp import osm2pgsql

SYSTEM_RAM_GB_MAIN = 64
OSM_PBF_GB_US = 10.4

class Osm2pgsqlTests(unittest.TestCase):

    ########################################
    # Class attribute types
    def test_osm2pgsql_recommendation_osm2pgsql_cache_max_type_float(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_cache_max
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_noslim_cache_type_float(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_noslim_cache
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_slim_cache_type_float(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_slim_cache
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_run_in_ram_type_bool(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_run_in_ram
        expected = bool
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_type_int(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec._get_cache_mb()
        expected = int    
        self.assertEqual(expected, type(result))



    def test_osm2pgsql_recommendation_osm2pgsql_cache_max_value(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_cache_max
        expected = 42.24
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_noslim_cache_value(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_noslim_cache
        expected = 27.0
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_slim_cache_value(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_slim_cache
        expected = 20.25
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_run_in_ram_value(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_run_in_ram
        expected = True
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec._get_cache_mb()
        expected = 20736
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_false(self):
        rec = osm2pgsql.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_drop
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_false_with_append(self):
        # NOTE: Setting system ram == PBF size to ensure slim is used
        rec = osm2pgsql.recommendation(system_ram_gb=OSM_PBF_GB_US,
                                       osm_pbf_gb=OSM_PBF_GB_US,
                                       append=True)
        result = rec.osm2pgsql_drop
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_true_without_append(self):
        # NOTE: Setting system ram == PBF size to ensure slim is used
        rec = osm2pgsql.recommendation(system_ram_gb=OSM_PBF_GB_US,
                                       osm_pbf_gb=OSM_PBF_GB_US,
                                       append=False)
        result = rec.osm2pgsql_drop
        expected = True
        self.assertEqual(expected, result)

