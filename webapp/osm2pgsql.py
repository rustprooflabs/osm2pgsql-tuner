"""Contains osm2pgsql class to help provide osm2pgsql tuning advice.

Requires osm2pgsql v1.5.0 or newer
"""
from webapp import config


class recommendation(object):

    def __init__(self, system_ram_gb, osm_pbf_gb, append=False,
                 pgosm_layer_set='run-all', ssd=True):
        """osm2pgsql.recommendation class takes basic inputs to generate
        command suggestions for osm2pgsql.

        Parameters
        -----------------------
        system_ram_gb : float
            How much total RAM the server has, in GB.

        osm_pbf_gb : float
            Size of the .osm.pbf file in GB.

        append : bool
            (Default False) If append mode is needed, --slim must be used.
        """
        # Set from params
        self.system_ram_gb = system_ram_gb
        self.osm_pbf_gb = osm_pbf_gb
        self.append = append
        self.pgosm_layer_set = pgosm_layer_set
        self.ssd = ssd

        # Calculated attributes
        self.osm2pgsql_cache_max = self._calculate_max_osm2pgsql_cache()
        self.osm2pgsql_noslim_cache = self._calculate_osm2pgsql_noslim_cache()
        # No real method to this calculation, initial gut instinct
        self.osm2pgsql_slim_cache = 0.75 * self.osm2pgsql_noslim_cache

        self.osm2pgsql_run_in_ram = self._run_in_ram()
        self.osm2pgsql_drop = self._use_drop()
        self.osm2pgsql_flat_nodes = self._use_flat_nodes()

        self.osm2pgsql_limited_ram = self._limited_ram_check()


    def _limited_ram_check(self):
        """Indicates if osm2pgsql could use more RAM than the system has available.
        """
        if self.osm2pgsql_run_in_ram:
            # If running w/out slim is possible, already determined there is
            # enough RAM.
            return False
        elif self.osm2pgsql_slim_cache > self.osm2pgsql_cache_max:
            return True

        return False

    def _use_flat_nodes(self):
        """Returns `True` if `--flat-nodes` should be used.

        Use `--flat-nodes` when:
            * PBF size is larger than config'd threshold AND SSD
            * PBF >= 30 GB (regardless of SSD)

        If the load can run entirely in-memory, no need to use flat nodes.

        Returns
        ---------------------
        use_flat_nodes : bool
        """
        if self.osm2pgsql_run_in_ram:
            return False
        elif self.osm_pbf_gb >= config.FLAT_NODES_THRESHOLD_GB and self.ssd:
            return True
        elif self.osm_pbf_gb >= 30.0:
            return True
        return False


    def _use_drop(self):
        """Checks other parameters to determine if --drop should be used.

        Returns
        -----------------------
        use_drop : bool
        """
        if not self.osm2pgsql_run_in_ram and not self.append:
            use_drop = True
        else:
            use_drop = False

        return use_drop


    def _calculate_max_osm2pgsql_cache(self):
        """Calculates the max RAM server has available to dedicate to osm2pgsql cache.

        Using 2/3 total as a starting point

		Returns
		-----------------------
		osm2pgsql_cache_max : float
        """
        osm2pgsql_cache_max = self.system_ram_gb * 0.66
        return osm2pgsql_cache_max

    def _calculate_osm2pgsql_noslim_cache(self):
        """
        https://blog.rustprooflabs.com/2021/05/osm2pgsql-reduced-ram-load-to-postgis

        Returns
        --------------------
        required_gb : float
            Value of memory (in GB) estimated for osm2pgsql to run w/out slim mode.
        """
        required_gb = 1 + (2.5 * self.osm_pbf_gb)
        return required_gb

    def _run_in_ram(self):
        """Determines if bypassing --slim is an option with the given details.

        Returns
        --------------------
        in_ram_possible : bool
        """
        if self.append:
            in_ram_possible = False
        elif self.osm2pgsql_noslim_cache <= self.osm2pgsql_cache_max:
            in_ram_possible = True
        else:
            in_ram_possible = False
        return in_ram_possible


    def get_osm2pgsql_command(self, out_format, pbf_filename):
        cmd = 'osm2pgsql -d $PGOSM_CONN \ \n'

        if self.osm2pgsql_run_in_ram:
            pass # Nothing to do here
        else:
            cache = self._get_cache_mb()
            cmd += f' --cache={cache} \ \n'
            cmd += ' --slim \ \n'
            if self.osm2pgsql_drop:
                cmd += ' --drop \ \n'
            if self.osm2pgsql_flat_nodes:
                cmd += ' --flat-nodes=/tmp/nodes \ \n'

        cmd += f' --output=flex --style=./{self.pgosm_layer_set}.lua \ \n'
        cmd += f' ~/pgosm-data/{pbf_filename}.osm.pbf'

        if out_format == 'api':
            cmd = cmd.replace('\ \n', '')
        elif out_format == 'html':
            cmd = cmd.replace('\n', '<br />')
        else:
            raise ValueError(f'Invalid out_format: {out_format}. Valid values are "api" and "html"')
        return cmd

    def _get_cache_mb(self):
        """ Only needed for slim mode"""
        if self.osm2pgsql_flat_nodes:
            cache = 0
        elif self.osm2pgsql_limited_ram:
            cache = int(self.osm2pgsql_cache_max * 1024)
        else:
            cache = int(self.osm2pgsql_slim_cache * 1024)

        return cache

    def _get_postgres_conf_suggestion(self):
        shared_buffers_gb = 1
        work_mem_mb = 50

        postgres_conf = {'shared_buffers': f'{shared_buffers_gb} GB',
                         'work_mem': f'{work_mem_mb} MB'}
        return postgres_conf
