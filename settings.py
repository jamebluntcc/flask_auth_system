import os


class Config(object):
    SECRET_KEY = os.environ.get('APP_SECRET', 'djajfkaafa')
    APP_DIR = os.path.abspath(os.path.dirname(os.path.join(__file__, 'app')))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)