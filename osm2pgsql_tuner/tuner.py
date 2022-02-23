"""Contains osm2pgsql class to help provide osm2pgsql tuning advice.

Recommendations require osm2pgsql v1.5.0 or newer
"""


FLAT_NODES_THRESHOLD_GB = 8.0
"""Sets threshold size for when to use --flat-nodes.

8-10 GB appears to be the threshold found prior to osm2pgsql v1.5.0.
Proper testing has not been done yet to prove this is the best threshold yet.
"""

class recommendation(object):

    def __init__(self, system_ram_gb, osm_pbf_gb, append=False,
                 pgosm_layer_set='run', ssd=True):
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
        if system_ram_gb < 2.0:
            raise ValueError('osm2pgsql requires a minimum of 2 GB RAM. See https://osm2pgsql.org/doc/manual.html#main-memory')

        self.system_ram_gb = system_ram_gb
        self.osm_pbf_gb = osm_pbf_gb
        self.append = append
        self.pgosm_layer_set = pgosm_layer_set
        self.ssd = ssd

        self.decisions = list()

        # Calculated attributes
        self.osm2pgsql_cache_max = self.calculate_max_osm2pgsql_cache()
        self.osm2pgsql_noslim_cache = self.calculate_osm2pgsql_noslim_cache()
        # No real method to this calculation, initial gut instinct
        self.osm2pgsql_slim_cache = 0.75 * self.osm2pgsql_noslim_cache

        self.osm2pgsql_run_in_ram = self.run_in_ram()
        self.osm2pgsql_drop = self.use_drop()
        self.osm2pgsql_flat_nodes = self.use_flat_nodes()

        self.osm2pgsql_limited_ram = self.limited_ram_check()


    def limited_ram_check(self):
        """Decide if osm2pgsql can use more RAM than the system has available.

        Returns
        -------------------------
        limited_ram : boolean
        """
        if self.osm2pgsql_run_in_ram:
            # If running w/out slim is possible, already determined there is
            # enough RAM.
            return False
        elif self.osm2pgsql_slim_cache > self.osm2pgsql_cache_max:
            return True

        # Is this possible to reach? Does self.osm2pgsql_run_in_ram provide
        # enough info already?
        return False

    def use_flat_nodes(self):
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
            decision = {'option': '--flat-node',
                        'name': 'Sufficient RAM',
                        'desc': 'No reason to consider --flat-nodes'}
            self.decisions.append(decision)
            return False
        elif self.osm_pbf_gb >= FLAT_NODES_THRESHOLD_GB and self.ssd:
            decision = {'option': '--flat-node',
                        'name': 'File of sufficient size',
                        'desc': 'File is large enough to consider --flat-nodes'}
            self.decisions.append(decision)
            return True
        elif self.osm_pbf_gb >= 30.0:
            decision = {'option': '--flat-node',
                        'name': 'File of sufficient size',
                        'desc': 'File is large enough to consider --flat-nodes'}
            self.decisions.append(decision)
            return True

        decision = {'option': '--flat-node',
                    'name': 'Not using',
                    'desc': 'No reason to use --flat-nodes'}
        self.decisions.append(decision)
        return False


    def use_drop(self):
        """Checks other parameters to determine if --drop should be used.

        Returns
        -----------------------
        use_drop : bool
        """
        if self.osm2pgsql_run_in_ram:
            use_drop = False
            decision = {'option': '--drop',
                        'name': 'Sufficient RAM',
                        'desc': 'Import can run entirely in RAM, --drop not needed.'}
            self.decisions.append(decision)
        elif self.append:
            use_drop = False
            decision = {'option': '--drop',
                        'name': 'Using Append',
                        'desc': 'Using --append, cannot use --drop'}
            self.decisions.append(decision)
        else:
            use_drop = True
            decision = {'option': '--drop',
                        'name': 'Using Drop',
                        'desc': 'No reason not to use --drop'}
            self.decisions.append(decision)

        return use_drop


    def calculate_max_osm2pgsql_cache(self):
        """Calculates the max RAM server has available to dedicate to osm2pgsql cache.

        Using 2/3 total as a starting point

		Returns
		-----------------------
		osm2pgsql_cache_max : float
        """
        osm2pgsql_cache_max = self.system_ram_gb * 0.66
        return osm2pgsql_cache_max

    def calculate_osm2pgsql_noslim_cache(self):
        """Calculates cache required by osm2pgsql in order to run w/out slim.

        https://blog.rustprooflabs.com/2021/05/osm2pgsql-reduced-ram-load-to-postgis

        Returns
        --------------------
        required_gb : float
            Value of memory (in GB) estimated for osm2pgsql to run w/out slim mode.
        """
        required_gb = 1 + (2.5 * self.osm_pbf_gb)
        return required_gb


    def run_in_ram(self):
        """Determines if bypassing --slim is an option with the given details.

        Returns
        --------------------
        in_ram_possible : bool
        """
        if self.append:
            in_ram_possible = False
            decision = {'option': '--slim',
                        'name': 'Using Append',
                        'desc': 'Use of --append mode requires --slim'}
            self.decisions.append(decision)
        elif self.osm2pgsql_noslim_cache <= self.osm2pgsql_cache_max:
            in_ram_possible = True
        else:
            in_ram_possible = False
        return in_ram_possible


    def get_osm2pgsql_command(self, out_format, pbf_path):
        """Builds the recommended osm2pgsql command.

        Parameters
        -----------------------
        out_format : str
            Either `api` or `html`.
        pbf_path : str

        Returns
        -----------------------
        cmd : str
        """
        cmd = 'osm2pgsql -d $PGOSM_CONN \ \n'

        if self.osm2pgsql_run_in_ram:
            pass # Nothing to do here
        else:
            cache = self.get_cache_mb()
            cmd += f' --cache={cache} \ \n'
            cmd += ' --slim \ \n'
            if self.osm2pgsql_drop:
                cmd += ' --drop \ \n'
            if self.osm2pgsql_flat_nodes:
                cmd += ' --flat-nodes=/tmp/nodes \ \n'

        cmd += f' --output=flex --style=./{self.pgosm_layer_set}.lua \ \n'
        cmd += f' {pbf_path}'

        if out_format == 'api':
            cmd = cmd.replace('\ \n', '')
        elif out_format == 'html':
            cmd = cmd.replace('\n', '<br />')
        else:
            raise ValueError(f'Invalid out_format: {out_format}. Valid values are "api" and "html"')
        return cmd


    def get_cache_mb(self):
        """Returns cache size to set in MB.

        Only needed for slim mode

        Returns
        ----------------------
        cache : int
            Size in MB to set --cache
        """
        if self.osm2pgsql_flat_nodes:
            cache = 0
            decision = {'option': '--cache',
                        'name': 'Using --flat-nodes',
                        'desc': 'Set --cache 0.'}
        elif self.osm2pgsql_limited_ram:
            cache = int(self.osm2pgsql_cache_max * 1024)
            decision = {'option': '--cache',
                        'name': 'Limited RAM',
                        'desc': 'Setting --cache to max available.'}
        else:
            cache = int(self.osm2pgsql_slim_cache * 1024)
            decision = {'option': '--cache',
                        'name': 'Sufficient RAM',
                        'desc': 'Set --cache to expected requirement for given PBF size.'}

        self.decisions.append(decision)
        return cache


    def _get_postgres_conf_suggestion(self):
        shared_buffers_gb = 1
        work_mem_mb = 50

        postgres_conf = {'shared_buffers': f'{shared_buffers_gb} GB',
                         'work_mem': f'{work_mem_mb} MB'}
        return postgres_conf
