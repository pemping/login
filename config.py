# import os


class DefaultConfig:
    SECRET_KEY = 'liyong'
    MONGODB_DB = 'test'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    BOOTSTRAP_SERVE_LOCAL = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '54004267@qq.com'
    MAIL_PASSWORD = 'bixhcaojqtoabgbe'
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(DefaultConfig):
    DEBUG = True

config = {'default': DefaultConfig, 'develop': DevelopConfig}
