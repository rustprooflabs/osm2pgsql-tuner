""" Unit tests to cover the pgconfig module."""
import unittest
from osm2pgsql_tuner import tuner


SYSTEM_RAM_GB_MAIN = 64
SYSTEM_RAM_GB_SMALL = 1
OSM_PBF_GB_US = 10.4

OSM_PBF_GB_CO = 0.2
OSM_PBF_GB_USWEST = 1.99 # Scaled below the 2GB threshold...
OSM_PBF_GB_ALWAYS_FLAT_FILE = 30.1 # Should always use flat file, even w/out SSD


class Osm2pgsqlTests(unittest.TestCase):

    ########################################
    # Class attribute types
    def test_osm2pgsql_recommendation_osm2pgsql_cache_max_type_float(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_cache_max
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_noslim_cache_type_float(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_noslim_cache
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_slim_cache_type_float(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_slim_cache
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_run_in_ram_type_bool(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_run_in_ram
        expected = bool
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_type_int(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.get_cache_mb()
        expected = int    
        self.assertEqual(expected, type(result))



    def test_osm2pgsql_recommendation_osm2pgsql_cache_max_value(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_cache_max
        expected = 42.24
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_noslim_cache_value(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_noslim_cache
        expected = 27.0
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_slim_cache_value(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_slim_cache
        expected = 20.25
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_run_in_ram_value(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_run_in_ram
        expected = True
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.get_cache_mb()
        expected = 20736
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_false(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_drop
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_false_with_append(self):
        # NOTE: Setting system ram == PBF size to ensure slim is used
        rec = tuner.recommendation(system_ram_gb=OSM_PBF_GB_US,
                                       osm_pbf_gb=OSM_PBF_GB_US,
                                       append=True)
        result = rec.osm2pgsql_drop
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_true_without_append(self):
        # NOTE: Setting system ram == PBF size to ensure slim is used
        rec = tuner.recommendation(system_ram_gb=OSM_PBF_GB_US,
                                       osm_pbf_gb=OSM_PBF_GB_US,
                                       append=False)
        result = rec.osm2pgsql_drop
        expected = True
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_false_with_plenty_of_ram(self):
        rec = tuner.recommendation(system_ram_gb=SYSTEM_RAM_GB_MAIN,
                                       osm_pbf_gb=OSM_PBF_GB_US)
        result = rec.osm2pgsql_flat_nodes
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_false_when_pbf_small(self):
        rec = tuner.recommendation(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                       osm_pbf_gb=OSM_PBF_GB_CO)
        result = rec.osm2pgsql_flat_nodes
        expected = False
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_true(self):
        rec = tuner.recommendation(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                       osm_pbf_gb=OSM_PBF_GB_US)
        result = rec.osm2pgsql_flat_nodes
        expected = True
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_true_no_ssd_when_pbf_gt30(self):
        rec = tuner.recommendation(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                       osm_pbf_gb=OSM_PBF_GB_ALWAYS_FLAT_FILE,
                                       ssd=False)
        result = rec.osm2pgsql_flat_nodes
        expected = True
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value_zero_with_flat_nodes(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_SMALL, OSM_PBF_GB_US)
        result = rec.get_cache_mb()
        expected = 0
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value_limited_ram_version(self):
        rec = tuner.recommendation(SYSTEM_RAM_GB_SMALL, OSM_PBF_GB_USWEST)
        result = rec.get_cache_mb()
        expected = 675
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_calculate_max_osm2pgsql_cache_works_with_float(self):
        value_specific = float(SYSTEM_RAM_GB_SMALL)
        rec = tuner.recommendation(value_specific, OSM_PBF_GB_USWEST)
        actual = rec._calculate_max_osm2pgsql_cache()
        expected = 0.66
        self.assertEqual(expected, actual)


    def test_osm2pgsql_recommendation_osm2pgsql_calculate_max_osm2pgsql_cache_works_with_integer(self):
        value_specific = int(SYSTEM_RAM_GB_SMALL)
        rec = tuner.recommendation(value_specific, OSM_PBF_GB_USWEST)
        actual = rec._calculate_max_osm2pgsql_cache()
        expected = 0.66
        self.assertEqual(expected, actual)

