import os


APP_NAME = 'osm2pgsql-tuner'

CURR_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.path.abspath(os.path.join(CURR_PATH, os.pardir))

try:
    LOG_PATH = os.environ['LOG_PATH']
except KeyError:
    LOG_PATH = PROJECT_BASE_PATH + '/webapp.log'


# Required for CSRF protection in Flask, please change to something secret!
try:
    APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
except KeyError:
    ERR_MSG = '\nSECURITY WARNING: To ensure security please set the APP_SECRET_KEY'
    ERR_MSG += ' environment variable.\n'
    #LOGGER.warning(ERR_MSG)
    print(ERR_MSG)
    APP_SECRET_KEY = 'S$332sgaasgklMGSU89y2gslkmlLLd vlmssajfsdgGADAAJjd77j@neHMl'



try:
    APP_DEBUG_RAW = os.environ['APP_DEBUG']
    if APP_DEBUG_RAW == 'False':
        APP_DEBUG = False
    else:
        APP_DEBUG = True
except KeyError:
    APP_DEBUG = True

DEFAULT_PBF_FILENAME = 'colorado-latest'

PBF_GB_SIZES = {'Colorado': {'size_gb': 0.203, 'filename': 'colorado-latest'},
                'California': {'size_gb': 0.893, 'filename': 'california-latest'},
                'Norway': {'size_gb': 1, 'filename': 'norway-latest'},
                'Germany': {'size_gb': 3.4, 'filename': 'germany-latest'},
                'Africa': {'size_gb': 4.5, 'filename': 'africa-latest'},
                'North America': {'size_gb': 10.4, 'filename': 'north-america-latest'},
                'Europe': {'size_gb': 23.4, 'filename': 'europe-latest'},
                'Planet': {'size_gb': 59.0, 'filename': 'planet-latest'}
                }
"""Regional PBF sizes for reference based on details from
Geofabrik's download server on 5/15/2021.

Planet PBF size from https://planet.openstreetmap.org/pbf/ on 7/21/2021.
"""

FLAT_NODES_THRESHOLD_GB = 8.0
