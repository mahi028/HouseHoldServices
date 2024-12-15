from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()
class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    JWT_COOKIE_CSRF_PROTECT = True
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_SECRET_KEY')
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    UPLOAD_FOLDER = 'application/static/upload'
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')

class DevelopmentConfig(Config):
    JWT_COOKIE_SECURE = False
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    JWT_COOKIE_SECURE = True # Will allow jwt cookies to be sent only over https.
    DEBUG = False
    ENV = 'production'