import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-really-big-secret'
    SERVABLE_POSTCODES = 'app/data/allowed_postcodes.json'
    SERVABLE_LOCAL_AUTHORITIES = 'app/data/allowed_local_authorities.json'


class Testing(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
