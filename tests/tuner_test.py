""" Unit tests to cover the pgconfig module."""
import unittest
from osm2pgsql_tuner import tuner

# Load configurables for tests
from .test_params import *



class Osm2pgsqlTests(unittest.TestCase):

    ########################################
    # Class attribute types
    def test_osm2pgsql_recommendation_osm2pgsql_cache_max_type_float(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_cache_max
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_noslim_cache_type_float(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_noslim_cache
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_slim_cache_type_float(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_slim_cache
        expected = float
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_run_in_ram_type_bool(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_run_in_ram
        expected = bool
        self.assertEqual(expected, type(result))

    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_type_int(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.get_cache_mb()
        expected = int    
        self.assertEqual(expected, type(result))



    def test_osm2pgsql_recommendation_osm2pgsql_cache_max_value(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_cache_max
        expected = 42.24
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_noslim_cache_value(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_noslim_cache
        expected = 27.0
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_slim_cache_value(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_slim_cache
        expected = 20.25
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_run_in_ram_value(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_run_in_ram
        expected = True
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.get_cache_mb()
        expected = 20736
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_value_error_when_insufficient_ram(self):
        with self.assertRaises(ValueError):
            tuner.Recommendation(SYSTEM_RAM_GB_TOO_SMALL, OSM_PBF_GB_CO)


    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_false(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        result = rec.osm2pgsql_drop
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_slim_no_drop_with_additional_param_raises_ValueError(self):
        with self.assertRaises(ValueError):
            tuner.Recommendation(system_ram_gb=OSM_PBF_GB_US,
                                 osm_pbf_gb=OSM_PBF_GB_US,
                                 slim_no_drop=True)

    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_false_with_slim_no_drop(self):
        # NOTE: Setting system ram == PBF size to ensure slim is used
        rec = tuner.Recommendation(system_ram_gb=OSM_PBF_GB_US,
                                       osm_pbf_gb=OSM_PBF_GB_US,
                                       slim_no_drop=True, append_first_run=True)
        result = rec.osm2pgsql_drop
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_drop_value_true_without_slim_no_drop(self):
        # NOTE: Setting system ram == PBF size to ensure slim is used
        rec = tuner.Recommendation(system_ram_gb=OSM_PBF_GB_US,
                                       osm_pbf_gb=OSM_PBF_GB_US,
                                       slim_no_drop=False)
        result = rec.osm2pgsql_drop
        expected = True
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_false_with_plenty_of_ram(self):
        rec = tuner.Recommendation(system_ram_gb=SYSTEM_RAM_GB_MAIN,
                                       osm_pbf_gb=OSM_PBF_GB_US)
        result = rec.osm2pgsql_flat_nodes
        expected = False
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_false_when_pbf_small(self):
        rec = tuner.Recommendation(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                       osm_pbf_gb=OSM_PBF_GB_CO)
        result = rec.osm2pgsql_flat_nodes
        expected = False
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_true(self):
        rec = tuner.Recommendation(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                       osm_pbf_gb=OSM_PBF_GB_US)
        result = rec.osm2pgsql_flat_nodes
        expected = True
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_flat_nodes_value_true_no_ssd_when_pbf_gt30(self):
        rec = tuner.Recommendation(system_ram_gb=SYSTEM_RAM_GB_SMALL,
                                       osm_pbf_gb=OSM_PBF_GB_ALWAYS_FLAT_FILE,
                                       ssd=False)
        result = rec.osm2pgsql_flat_nodes
        expected = True
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value_zero_with_flat_nodes(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_SMALL, OSM_PBF_GB_US)
        result = rec.get_cache_mb()
        expected = 0
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_cache_mb_value_limited_ram_version(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_SMALL, OSM_PBF_GB_USWEST)
        result = rec.get_cache_mb()
        expected = 1351
        self.assertEqual(expected, result)


    def test_osm2pgsql_recommendation_osm2pgsql_calculate_max_osm2pgsql_cache_works_with_float(self):
        value_specific = float(SYSTEM_RAM_GB_SMALL)
        rec = tuner.Recommendation(value_specific, OSM_PBF_GB_USWEST)
        actual = rec.calculate_max_osm2pgsql_cache()
        expected = 1.32
        self.assertEqual(expected, actual)


    def test_osm2pgsql_recommendation_osm2pgsql_calculate_max_osm2pgsql_cache_works_with_integer(self):
        value_specific = int(SYSTEM_RAM_GB_SMALL)
        rec = tuner.Recommendation(value_specific, OSM_PBF_GB_USWEST)
        actual = rec.calculate_max_osm2pgsql_cache()
        expected = 1.32
        self.assertEqual(expected, actual)


    def test_osm2pgsql_recommendation_osm2pgsql_get_osm2pgsql_command_value_not_in_ram(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_SMALL, OSM_PBF_GB_US)
        pbf_path = 'blahblah'
        result = rec.get_osm2pgsql_command(pbf_path=pbf_path)
        expected = f'osm2pgsql -d $PGOSM_CONN  --cache=0  --slim  --drop  --flat-nodes=/tmp/nodes  --create  --output=flex --style=./run.lua  {pbf_path}'
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_get_osm2pgsql_command_value_is_in_ram(self):
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US)
        pbf_path = 'blahblah'
        result = rec.get_osm2pgsql_command(pbf_path=pbf_path)
        expected = f'osm2pgsql -d $PGOSM_CONN  --create  --output=flex --style=./run.lua  {pbf_path}'
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_command_append_first_run_correct_cmd(self):
        slim_no_drop = True
        append_first_run = True
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US,
                                   slim_no_drop=slim_no_drop,
                                   append_first_run=append_first_run)
        pbf_path = 'blahblah'
        result = rec.get_osm2pgsql_command(pbf_path=pbf_path)
        expected = f'osm2pgsql -d $PGOSM_CONN  --cache=0  --slim  --flat-nodes=/tmp/nodes  --create  --output=flex --style=./run.lua  {pbf_path}'
        self.assertEqual(expected, result)

    def test_osm2pgsql_recommendation_osm2pgsql_command_append_subsequent_run_correct_cmd(self):
        slim_no_drop = True
        append_first_run = False
        rec = tuner.Recommendation(SYSTEM_RAM_GB_MAIN, OSM_PBF_GB_US,
                                   slim_no_drop=slim_no_drop,
                                   append_first_run=append_first_run)
        pbf_path = 'blahblah'
        result = rec.get_osm2pgsql_command(pbf_path=pbf_path)
        expected = f'osm2pgsql -d $PGOSM_CONN  --cache=0  --slim  --flat-nodes=/tmp/nodes  --append  --output=flex --style=./run.lua  {pbf_path}'
        self.assertEqual(expected, result)
