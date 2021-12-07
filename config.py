from logging.config import dictConfig
import os

import pathlib
from pathlib import Path
import logging
import json

# Flask
fastapi_host = "0.0.0.0"
fastapi_port = 5000
debug = True
reload = True


# For a good understanding on config
# See: https://www.toptal.com/python/in-depth-python-logging#:~:text=There%20are%20six%20log%20levels,particularity%20will%20be%20addressed%20next.
# Logging

from logging.config import dictConfig


dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(dir_path)
# For a good understanding on config
# See: https://www.toptal.com/python/in-depth-python-logging#:~:text=There%20are%20six%20log%20levels,particularity%20will%20be%20addressed%20next.
# Logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
        },
        'info': {
            'format': '[%(asctime)s]: %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'app.log',
            'when': 'D',
            'interval': 7
        },
        'debugfilehandler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'app.log',
            'formatter': 'default',
            'when': 'D',
            'interval': 7
        },
        'consoledebughandler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'consolehandler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'info'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['debugfilehandler', 'consolehandler'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'console': {
            'handlers': ['consoledebughandler', 'debugfilehandler'],
            'level': 'DEBUG',
            'propogate': True
        },
        'consoleonly': {
            'handlers': ['consoledebughandler'],
            'level': 'DEBUG',
            'propogate': True
        }
    }
}
dictConfig(LOGGING_CONFIG)

default_log = logging.getLogger('console')

common_date_format = "%d-%m-%Y %H:%M"

max_retries = 3


# Use secrets.json if running on server
secrets_path = os.getenv('SECRETS_PATH', '/home/ubuntu/secrets.json') # Default is /home/ubuntu/secrets.json
# postgres
postgres_username = 'postgres'
postgres_password = 'dhaval'
postgres_db_name = "demark"
postgres_host = "127.0.0.1"
postgres_port = 5432


secrets_file = Path("secrets.json")

if secrets_file.is_file():
    secrets = ''
    with open(secrets_file) as f:
        secrets = json.loads(f.read())

        user_id = secrets['user_id']
        password = secrets['password']
        account_id = secrets['account_id']
        postgres_username = secrets['postgres_username']
        postgres_password = secrets['postgres_password']
        postgres_db_name = secrets['postgres_db_name']
        postgres_host = secrets['postgres_host']
        postgres_port = secrets['postgres_port']
        app_name = secrets['app_name']
        app_version =  secrets['app_version']

sqlalchemy_database_uri = f"postgresql://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}"
