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
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379 
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '1b8a6945cd4f54'
    MAIL_PASSWORD = 'c2d0794ed7c53c'
    MAIL_DEFAULT_SENDER = 'abc@gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class DevelopmentConfig(Config):
    JWT_COOKIE_SECURE = False
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    JWT_COOKIE_SECURE = True # Will allow jwt cookies to be sent only over https.
    DEBUG = False
    ENV = 'production'