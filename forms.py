from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Length, Email

from modelosBanco import Tarefa

# awo
class FormularioRegistro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=4, max=25)])
    email = EmailField('Email',  validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    registrar = SubmitField('Registrar')

class FormularioLogin(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    login = SubmitField('Login')

class FormularioTarefa(FlaskForm):
    nome_tarefa = StringField('Nome', validators=[DataRequired()])
    data_tarefa = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('pendente', 'Pendente'), ('em andamento', 'Em Andamento'),
                                            ('concluída', 'Concluída')], default='pendente')
    usuarios = SelectMultipleField('Usuários', choices=[])  # Este campo será preenchido dinamicamente
    criar = SubmitField('Criar Evento')

    def __init__(self, user_choices, *args, **kwargs):
        super(FormularioTarefa, self).__init__(*args, **kwargs)
        self.usuarios.choices = user_choices

class FormularioEditarTarefa(FlaskForm):
    nome_tarefa = StringField('Nome', validators=[DataRequired()])
    data_tarefa = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('pendente', 'Pendente'), ('em andamento', 'Em Andamento'), ('concluída', 'Concluída')])
    editar = SubmitField('Editar Evento')