import os
from pathlib import Path

# PATHS
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = str(Path(SETTINGS_DIR).parents[1])
SIMBAD_DATA_PATH = os.getenv(
    'SIMBAD_DATA_PATH',
    '{}/data'.format(str(Path(SETTINGS_DIR).parents[2]))
)
CLI_PATH = ROOT_PATH + '/bin/simbad-cli'
OUT_PATH = ROOT_PATH + '/output'

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/simbad.db'.format(SIMBAD_DATA_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'