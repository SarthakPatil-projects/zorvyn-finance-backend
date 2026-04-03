from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'zorvyn-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'zorvyn-jwt-secret'

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.records import records_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(records_bp, url_prefix='/records')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app