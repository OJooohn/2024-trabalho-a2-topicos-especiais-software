from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Length, Email
# awo
class FormularioRegistro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=4, max=25)])
    email = EmailField('Email',  validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    registrar = SubmitField('Registrar')

class FormularioLogin(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    login = SubmitField('Login')

class FormularioEvento(FlaskForm):
    nome_evento = StringField('Nome', validators=[DataRequired()])
    data_evento = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('pendente'), ('em andamento'), ('concluída')], default='pendente')
    criar = SubmitField('Criar Evento')

class FormularioEditarEvento(FlaskForm):
    nome_evento = StringField('Nome', validators=[DataRequired()])
    data_evento = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('pendente'), ('em andamento'), ('concluída')], default='pendente')
    criar = SubmitField('Editar Evento')

class FormularioAtualizarEvento(FlaskForm):
    status = SelectField('Status', choices=[('pendente'), ('em andamento'), ('concluída')])
    atualizar = SubmitField('Atualizar')