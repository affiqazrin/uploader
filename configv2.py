import os
from urllib.parse import quote
import uuid

# Define the base directory of your project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(uuid.uuid4())
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for better performance

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rbpadmin:%s@10.12.215.45:3306/prpdb_devl' % quote('rbp0rt@l1')
    # Other development configurations...

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rbpadmin:%s@10.12.215.45:3306/prpdb_prod' % quote('rbp0rt@l1')
    # Other production configurations...

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance//svr.db'
    # Other test configurations...

# LDAP configuration
class LDAPConfig:
    LDAP_SERVER = os.environ.get('LDAP_SERVER') or 'ldap://ambankgroup.ahb.com'
    LDAP_BIND_USER = os.environ.get('LDAP_BIND_USER') or 'CN=svsrbportal,OU=Service Account,DC=AMBANKGROUP,DC=AHB,DC=COM'
    LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD') or 'Merah12#'
    LDAP_SEARCH_BASE = os.environ.get('LDAP_SEARCH_BASE') or 'OU=AMB,OU=Employee,DC=ambankgroup,DC=ahb,DC=com'

# Define a dictionary to easily select the appropriate configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': ProductionConfig  # Default configuration
}
