import os


class Config(object):
    SECRET_KEY = os.environ.get('APP_SECRET', 'djajfkaafa')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    APP_DIR = os.path.abspath(os.path.dirname(os.path.join(__file__, 'app')))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['MAIL_USER']
    MAIL_PASSWORD = os.environ['MAIL_PASSWD']
    MAIL_SUBJECT_PREFIX = '[JAMEBLUNTCC]'
    MAIL_SENDER = 'Chencheng flask admin <{0}>'.format(MAIL_USERNAME)
    MAIL_MAP = {
        '163.com': 'https://mail.163.com',
        'qq.com': 'https://mail.qq.com'
    }
    ALLOWED_EXTENSIONS = ['doc', 'docx']
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'app', 'static', 'upload')
    OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, 'app', 'static', 'output')


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DB_NAME = 'test.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


config = {'test': TestConfig,
          'dev': DevConfig}
