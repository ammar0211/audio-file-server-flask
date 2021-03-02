# Flask configuration variables.
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
