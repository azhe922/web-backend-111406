import os
from datetime import timedelta
class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = os.getenv('db_host')
    SECRET_KEY = os.getenv('secret_key')
    JSON_AS_ASCII = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    DB_HOST = os.getenv('db_host')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class CloudServiceConfig(ProductionConfig):

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)


config = {
    'development': Config,
    'production': ProductionConfig,
    'cloud': CloudServiceConfig,

    'default': Config
}