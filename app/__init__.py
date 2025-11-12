# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig, TestingConfig
from flask_migrate import Migrate
from flask_wtf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  

def create_app(config_name="development"):
    app = Flask(__name__)

    # Choose config
    if config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    csrf = CSRFProtect()
    csrf.init_app(app)

    # Register blueprints
    from app.auth.routes import auth
    from app.main.routes import main
    from app.analyst.routes import analyst
    from app.viewer.routes import viewer
    from app.api.chat import chat_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(analyst)
    app.register_blueprint(viewer)
    app.register_blueprint(chat_bp)

    csrf.exempt(chat_bp)

    return app
