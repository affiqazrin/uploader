# config.py

import os
from urllib.parse import quote  

# Define the base directory of your project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rbpadmin:%s@10.12.215.45:3306/prpdb_prod' % quote('rbp0rt@l1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for better performance

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rbpadmin:%s@10.12.215.45:3306/prpdb_devl' % quote('rbp0rt@l1')  # Development schema
    SQLALCHEMY_POOL_SIZE = 5  # Number of connections in the pool for testing
    SQLALCHEMY_POOL_TIMEOUT = 30  # Connection pool timeout for testing (seconds)
    SQLALCHEMY_POOL_RECYCLE = 1800  # Recycle connections after 30 minutes
    SQLALCHEMY_POOL_PRE_PING = False  # Disable pre-pinging for testing
    SQLALCHEMY_ECHO = True  # Set to True for debugging in testing

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rbpadmin:%s@10.12.215.45:3306/prpdb_prod' % quote('rbp0rt@l1')  # Production schema
    SQLALCHEMY_POOL_SIZE = None  # Number of connections in the pool for production
    SQLALCHEMY_POOL_TIMEOUT = None  # Connection pool timeout for production (seconds)
    SQLALCHEMY_POOL_RECYCLE = 3600  # Recycle connections after 1 hour
    SQLALCHEMY_POOL_PRE_PING = True  # Enable pre-pinging for production
    SQLALCHEMY_ECHO = False  # Typically set to False for production

# SQLite configuration for testing purposes only
class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance//svr.db'  # SQLite database for testing
    SQLALCHEMY_POOL_SIZE = 5  # Number of connections in the pool for testing
    SQLALCHEMY_POOL_TIMEOUT = 30  # Connection pool timeout for testing (seconds)
    SQLALCHEMY_POOL_RECYCLE = 1800  # Recycle connections after 30 minutes
    SQLALCHEMY_POOL_PRE_PING = False  # Disable pre-pinging for testing
    SQLALCHEMY_ECHO = True  # Set to True for debugging in testing



# Define a dictionary to easily select the appropriate configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': ProductionConfig  # Default configuration
}


LDAP_SERVER = 'ldap://ambankgroup.ahb.com'
LDAP_BIND_USER = 'CN=svsrbportal,OU=Service Account,DC=AMBANKGROUP,DC=AHB,DC=COM'
LDAP_BIND_PASSWORD = 'Merah12#'
LDAP_SEARCH_BASE = 'OU=AMB,OU=Employee,DC=ambankgroup,DC=ahb,DC=com'

SECRET_KEY = 'uuid.uuid1()'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///instance//svr.db'
