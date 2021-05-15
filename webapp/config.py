import os
import logging

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

PBF_GB_SIZES = {'Colorado': 0.203,
                'California': 0.893,
                'Norway': 1,
                'Germany': 3.4,
                'Africa': 4.5,
                'North America': 10.4,
                'Europe': 23.4}
"""PBF sizes for reference based on details from
Geofabrik's download server on 5/15/2021.
"""
