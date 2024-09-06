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
    eventos = db.relationship('Evento', backref='owner', lazy=True)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_evento = db.Column(db.String, nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pendente', 'em andamento', 'concluída'), default='pendente')
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)