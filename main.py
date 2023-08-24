from flask import Flask
from flask_login import LoginManager
from models.models import database, User

login_manager = LoginManager()

def load_config(app):
    app.config.from_object('config.Config')

def configure_login_manager(app):
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

def ini_database(app):
    database.init_app(app)
    with app.app_context():
        database.create_all()

def register_blueprints(app):
    from routes.routes import routes_bp
    from auth.auth import auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

def create_app():
    app = Flask(__name__)
    configure_login_manager(app)
    load_config(app)
    ini_database(app)
    register_blueprints(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)