from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register all blueprints
    from app.routes.auth import auth_bp
    from app.routes.farm_routes import farm_bp
    from app.routes.crop_routes import crop_bp
    from app.routes.livestock_routes import livestock_bp
    from app.routes.expenses_routes import expenses_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(farm_bp, url_prefix='/farms')
    app.register_blueprint(crop_bp, url_prefix='/crops')
    app.register_blueprint(livestock_bp)
    app.register_blueprint(expenses_bp)

    app.register_blueprint(dashboard_bp)


    return app
