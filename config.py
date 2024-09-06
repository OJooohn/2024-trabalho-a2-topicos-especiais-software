from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'DJ0519LVKFASHUI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message = 'Por favor, faça login para acessar a página!'
