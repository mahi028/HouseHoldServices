from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, JWTManager, set_access_cookies
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import os
from flask_caching import Cache
from flask_mail import Mail
import flask_excel as excel

db = SQLAlchemy()
migration = Migrate()
jwt = JWTManager()
csrf = CSRFProtect()
cache = Cache()
mail = Mail()

def create_app():
    app = Flask(__name__,
                static_folder=os.path.join(os.path.dirname(__file__), "static"),
                )
                
    from application.api import api
    api.init_app(app)

    CORS(app, origins=["http://localhost:5173", "http://localhost:8000"], supports_credentials=True)
    app.config.from_object(DevelopmentConfig) #Change DevelopmentConfig to ProductionConfig in production

    db.init_app(app)
    migration.init_app(app, db, render_as_batch=True)

    from application.modals import User

    #flask_jwt_extended setup
    jwt.init_app(app)

    csrf.init_app(app) #only for login and register form submissions


    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):        
        identity = jwt_data["sub"]
        return User.query.get(identity)

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=20))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response
        
    # #celery config    
    # celery_app = celery_init_app(app)

    #cache
    cache.init_app(app)
    app.app_context().push()

    #forMailservice
    mail.init_app(app)

    #for flask excel
    excel.init_excel(app)

    return app

