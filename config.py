# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#Define base config
class Config:
    #Set secret key for cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'HR-SECRET'
    #Database config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    #mail config
    HR_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = 'HR app <Hrapp@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    @staticmethod
    def init_app(app):
        pass

#dev config inherits from config class and also setup dev-database
class DevelopmentConfig(Config):
    DEBUG = True
    # move this to mail setup in the app folder
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "olusakintimmy@gmail.com"
    MAIL_PASSWORD = "Timothy12"
    # setup database for development
    SQLALCHEMY_DATABASE_URI =os.environ.get('DEV_DATABASE_URL') or \
                             'sqlite:///' + os.path.join(BASE_DIR, 'Socialapp-dev2.sqlite')

#test config importing from config folder
class TestConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, 'Social-app-test.sqlite')

# main production config
class ProductionConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, 'Social-app-prod.sqlite')

# create a generalized config dictionary
config = {
'development': DevelopmentConfig,
'testing': TestConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
