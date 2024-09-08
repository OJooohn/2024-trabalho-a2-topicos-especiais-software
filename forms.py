from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Length, Email

from modelosBanco import Tarefa

# awo

# Os nomes de cada formulario (nome, senha, email, registrar, login) é as labels e inputs colocados entre {{}} no arquivo .html

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

    # Será preenchido automaticamente, conforme os usuários cadastrados selecionados
    usuarios = SelectMultipleField('Usuários', choices=[])
    criar = SubmitField('Criar Tarefa')

    # Receberá os usuários, exceto o logado, para escolher a quem atribuir a tarefa
    def __init__(self, user_choices, *args, **kwargs):
        super(FormularioTarefa, self).__init__(*args, **kwargs)
        # Vai colocar no form 'usuarios', em sua propriedade (choices), os usuários cadstrados, exceto o logado
        self.usuarios.choices = user_choices

class FormularioEditarTarefa(FlaskForm):
    nome_tarefa = StringField('Nome', validators=[DataRequired()])
    data_tarefa = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')

    # Em choices, ('pendente', 'Pendente')
    # A primeira parte 'pendente' é o que será selecionado pelo usuário, o que será armazenado
    # A segunda parte 'Pendente' é a parte visível para o usuário, apenas por estética
    status = SelectField('Status', choices=[('pendente', 'Pendente'), ('em andamento', 'Em Andamento'), ('concluída', 'Concluída')])
    editar = SubmitField('Editar Tarefa')