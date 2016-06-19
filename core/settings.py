import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Application Settings
DEBUG = True
TESTING = False
SECRET_KEY = 'ChronosBestKeptSecret'
APPLICATION_ROOT = '/api'
SESSION_COOKIE_SECURE = True

# Database Settings
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/webapp'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
