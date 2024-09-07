from email.policy import default
from enum import unique

from flask_sqlalchemy import *

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from config import db, login_manager

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    tarefas = db.relationship('Tarefa', backref='owner', lazy=True)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_tarefa = db.Column(db.String(100), nullable=False)
    data_tarefa = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pendente')