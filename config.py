from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Necessário para a segurança do login, proteção de dados, autenticação
app.config['SECRET_KEY'] = 'DJ0519LVKFASHUI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'index'

# Usado quando é tentado entrar no dashoard pela URL, sem fazer login.
# Vai aparecer na mensagem usando a função flash do flask
login_manager.login_message = 'Por favor, faça login para acessar a página!'
