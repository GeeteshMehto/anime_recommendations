from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables early

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.anime.routes import anime_bp
    from app.user.routes import user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(anime_bp, url_prefix='/anime')
    app.register_blueprint(user_bp, url_prefix='/user')

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Define a basic route for the frontend
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Add global request logging
    @app.before_request
    def log_request():
        print(f"=== INCOMING REQUEST ===")
        print(f"Method: {request.method}")
        print(f"Path: {request.path}")
        print(f"URL: {request.url}")
        print(f"Headers: {dict(request.headers)}")
        if request.data:
            print(f"Body: {request.data}")
        print("========================")

    # Add response logging
    @app.after_request
    def log_response(response):
        print(f"=== RESPONSE ===")
        print(f"Status: {response.status}")
        print(f"Headers: {dict(response.headers)}")
        print("================")
        return response

    return app