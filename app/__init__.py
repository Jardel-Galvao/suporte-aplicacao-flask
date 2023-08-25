from flask import Flask
from flask_login import LoginManager
from .models.user import User
from .routes.routes import routes_bp
from .auth.auth import auth_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    configure_app(app)
    initialize_app(app)
    register_blueprints(app)

    return app

def configure_app(app):
    load_config(app)
    configure_login_manager(app)

def load_config(app):
    app.config.from_object('config.Config')

def configure_login_manager(app):
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

def initialize_app(app):
    initialize_database(app)

def initialize_database(app):
    from .models import database
    database.init_app(app)
    
    with app.app_context():
        database.create_all()

def register_blueprints(app):
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))