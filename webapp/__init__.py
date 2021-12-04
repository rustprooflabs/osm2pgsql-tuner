import logging
from flask import Flask
from webapp import config

# App settings
app = Flask(__name__)
app.config['DEBUG'] = config.APP_DEBUG
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = True

if config.APP_DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

logging.basicConfig(filename=config.LOG_PATH,
                    level=LOG_LEVEL,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


from webapp import routes
