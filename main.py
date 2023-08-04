from flask import Flask
from flask_login import LoginManager
from models.models import User, database

# Configurações do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Códigos Python/suporte-aplicacao-flask/instance/database.db'

# Inicialize o LoginManager com a aplicação Flask
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
database.init_app(app)

# Importe os blueprints e registre-os com a aplicação Flask
from routes.routes import routes_bp
app.register_blueprint(routes_bp)
from auth.auth import auth_bp
app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    database.create_all()

if __name__ == "__main__":
    app.run(debug=True)
