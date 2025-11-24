# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate
# from app.config import Config
#
# from models.user import User
# from models.farm import Farm
# from models.crop import Crop
# from models.livestock import Livestock
# from models.expenses import Expense
# from models.sale import Sale
#
# __all__ = ['User', 'Farm', 'Crop', 'Livestock', 'Expense', 'Sale']
#
# db = SQLAlchemy()
# bcrypt = Bcrypt()
# jwt = JWTManager()
# migrate = Migrate()
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     # Initialize extensions
#     db.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)
#     migrate.init_app(app, db)
#
#     # Import and register all blueprints
#     from app.routes.auth import auth_bp
#     from app.routes.farm_routes import farm_bp
#     from app.routes.crop_routes import crop_bp
#     from app.routes.livestock_routes import livestock_bp
#     from app.routes.expenses_routes import expenses_bp
#     from app.routes.dashboard import dashboard_bp
#     from app.routes.sales_routes import sales_bp
#
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(farm_bp, url_prefix='/farms')
#     app.register_blueprint(crop_bp, url_prefix='/crops')
#     app.register_blueprint(livestock_bp)
#     app.register_blueprint(expenses_bp)
#     app.register_blueprint(sales_bp)
#     app.register_blueprint(dashboard_bp)
#
#     return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register all blueprints INSIDE create_app()
    from app.routes.auth import auth_bp
    from app.routes.farm_routes import farm_bp
    from app.routes.crop_routes import crop_bp
    from app.routes.livestock_routes import livestock_bp
    from app.routes.expenses_routes import expenses_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.sales_routes import sales_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(farm_bp, url_prefix='/farms')
    app.register_blueprint(crop_bp, url_prefix='/crops')
    app.register_blueprint(livestock_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(dashboard_bp)

    return app