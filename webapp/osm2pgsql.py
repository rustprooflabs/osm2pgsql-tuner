"""Contains osm2pgsql class to help provide osm2pgsql tuning advice.
"""
"""Requires osm2pgsql commit 94dae34 or newer

    https://github.com/openstreetmap/osm2pgsql/commit/94dae34b7aa1463339cdb6768d28a6e8ee53ef65

    Assuming this will be included in v1.4.3 when it is tagged/released
"""


class recommendation(object):

    def __init__(self, system_ram_gb, osm_pbf_gb, append=False):
        """osm2pgsql.recommendation class takes basic inputs to generate command suggestions for osm2pgsql.

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
        self.pgosm_layer_set = 'run-all'
        
        # Calculated attributes
        self.osm2pgsql_cache_max = self._calculate_max_osm2pgsql_cache()
        self.osm2pgsql_noslim_cache = self._calculate_osm2pgsql_noslim_cache()
        self.osm2pgsql_slim_cache = 0.75 * self.osm2pgsql_noslim_cache # No real method to this calculation, initial gut instinct
        self.osm2pgsql_noslim = self._can_i_noslim()
        if not self.osm2pgsql_noslim and not self.append:
            self.osm2pgsql_drop = True
        else:
            self.osm2pgsql_drop = False
        self.osm2pgsql_limited_ram = self._limited_ram_check()


    def _limited_ram_check(self):
        """Indicates if osm2pgsql could use more RAM than the system has available.
        """
        if self.osm2pgsql_noslim:
            # If running w/out slim is possible, already determined there is 
            # enough RAM.
            return False
        elif self.osm2pgsql_slim_cache > self.osm2pgsql_cache_max:
            return True

        return False


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
    
    def _can_i_noslim(self):
        """Determines if bypassing --slim is an option with the given details.
        
        Returns
        --------------------
        noslim_possible : bool
        """
        if self.append:
            noslim_possible = False
        elif self.osm2pgsql_noslim_cache <= self.osm2pgsql_cache_max:
            noslim_possible = True
        else:
            noslim_possible = False
        return noslim_possible

    def get_osm2pgsql_command(self, out_format='nix'):
        cmd = 'osm2pgsql -d $PGOSM_CONN \ \n'
        
        if self.osm2pgsql_noslim:
            pass # Nothing to do here
        else:
            cache = self._get_cache_mb()
            cmd += f'    --cache={cache} \ \n'
            cmd += '    --slim \ \n'

        if self.osm2pgsql_drop:
            cmd += '    --drop \ \n'

        cmd += f'    --output=flex --style=./{self.pgosm_layer_set}.lua \ \n'
        cmd += '    ~/pgosm-data/your-input.osm.pbf'

        if out_format == 'nix':
            pass
        elif out_format == 'html':
            cmd = cmd.replace('\n', '<br />')
        else:
            raise ValueError(f'Invalid out_format: {out_format}. Valid values are nix and html')
        return cmd

    def _get_cache_mb(self):
        """ Only needed for slim mode"""
        if self.osm2pgsql_limited_ram:
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
    
    def print(self):
        print(f'Total RAM: {self.system_ram_gb} GB')
        print(f'RAM available for osm2pgsql cache: {self.osm2pgsql_cache_max} GB')
        
        if self.osm2pgsql_noslim:
            print('You can run w/out slim mode!')
            print(f'Cache size: {self.osm2pgsql_noslim_cache} GB ')
        else:
            print('Slim mode required')
            print(self.osm2pgsql_slim_cache)
                
        print(f'Source PBF Size: {self.osm_pbf_gb} GB')
        
        osm2pgsql_command = self.get_osm2pgsql_command()
        print()
        print(osm2pgsql_command)
        print()
        print('\nWhat about Postgres CONF ?')
        print(self._get_postgres_conf_suggestion())

