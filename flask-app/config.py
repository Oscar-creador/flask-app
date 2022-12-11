import os

class Config(object):
    SECRET_KEY = "my_secret_key"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/asistencia-flask'




