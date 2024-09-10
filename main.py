import time

from flask import Flask, render_template, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import update
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash

from config import app, db
from forms import FormularioLogin, FormularioTarefa, FormularioEditarTarefa
from modelosBanco import *

@app.route('/', methods=['GET', 'POST'])
def index():

    formsLogin = FormularioLogin()

    if formsLogin.validate_on_submit():
        usuarioNome = formsLogin.nome.data
        usuarioDB = Usuario.query.filter_by(nome=usuarioNome).first()

        if usuarioDB is None:
            flash(f'Usuário "{ usuarioNome }" não encontrado. Tente novamente')
        else:
            senhaDigitada = formsLogin.senha.data
            senhaDB = usuarioDB.senha

            if check_password_hash(senhaDB, senhaDigitada):
                login_user(usuarioDB)
                return redirect('dashboard')
            else:
                flash('Senha incorreta... Digite novamente')

    return render_template('index.html', form=formsLogin)

@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import FormularioRegistro
    from werkzeug.security import generate_password_hash

    formsRegistro = FormularioRegistro()

    if formsRegistro.validate_on_submit():
        usuarioNome = formsRegistro.nome.data
        usuarioEmail = formsRegistro.email.data
        usuarioSenha = generate_password_hash(formsRegistro.senha.data)

        if formsRegistro.senha.data == formsRegistro.confirmar_senha.data:

            usuarioExistente = Usuario.query.filter_by(nome=usuarioNome).first()
            emailExistente = Usuario.query.filter_by(email=usuarioEmail).first()

            if usuarioExistente:
                flash('Usuario ja cadastrado. Escolha outro nome de usuário!')
            elif emailExistente:
                flash('Email ja cadastrado. Digite outro email!')
            else:
                novo_usuario = Usuario(nome=usuarioNome, email=usuarioEmail, senha=usuarioSenha, is_admin=False)
                db.session.add(novo_usuario)
                db.session.commit()
                return redirect(url_for('index'))

        else:
            flash('Por favor, confirme a senha corretamente')

    return render_template('register.html', form=formsRegistro)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    nomeUsuario = current_user.nome

    filter_status = request.args.get('filter_status', '')

    is_admin = current_user.is_admin

    if is_admin:
        if filter_status:
            tarefas = db.session.query(Tarefa, Usuario).join(Usuario, Tarefa.id_usuario == Usuario.id).filter(Tarefa.status == filter_status).all()
        else:
            tarefas = db.session.query(Tarefa, Usuario).join(Usuario, Tarefa.id_usuario == Usuario.id).all()
    else:
        if filter_status:
            tarefas = db.session.query(Tarefa, Usuario).join(Usuario, Tarefa.id_usuario == Usuario.id).filter(Tarefa.id_usuario == current_user.id, Tarefa.status == filter_status).all()
        else:
            tarefas = db.session.query(Tarefa, Usuario).join(Usuario, Tarefa.id_usuario == Usuario.id).filter(Tarefa.id_usuario == current_user.id).all()

    # Obter todos os usuários, exceto o administrador
    usuarios = Usuario.query.filter(Usuario.is_admin == False).all()

    return render_template('dashboard.html', usuario=nomeUsuario, tarefas=tarefas, is_admin=is_admin, usuarios=usuarios)


@app.route('/criar_tarefa', methods=['GET', 'POST'])
def criar_tarefa():
    # Usuarios que não são o usuário logado
    # Aparecem na lista de seleção
    usuarios = Usuario.query.filter(Usuario.id != current_user.id, Usuario.is_admin == False).all()

    # Criando uma tupla com os usuários para a criação dos eventos
    usuarios_escolhidos = [(user.id, user.nome) for user in usuarios]

    # Passando a tupla para o formulário
    formulario = FormularioTarefa(user_choices=usuarios_escolhidos)

    if formulario.validate_on_submit():

        # Pegar os dados do formulário
        nomeEvento = formulario.nome_tarefa.data
        dataEvento = formulario.data_tarefa.data
        descEvento = formulario.descricao.data

        usuBanco = Usuario.query.filter_by(id=current_user.id).first()

        tarefa_banco = Tarefa.query.filter_by(nome_tarefa=nomeEvento).first()

        is_admin = Usuario.query.filter_by(id=current_user.id).first().is_admin

        if not is_admin:
            novo_evento = Tarefa(nome_tarefa=nomeEvento, data_tarefa=dataEvento, descricao=descEvento, id_usuario=usuBanco.id, status='pendente')
            db.session.add(novo_evento)
            db.session.commit()

        # Adicionar usuários selecionados ao evento
        for usuario_selecionado in formulario.usuarios.data:
            usuario = Usuario.query.get(usuario_selecionado)
            novo_evento = Tarefa(nome_tarefa=nomeEvento, data_tarefa=dataEvento, descricao=descEvento, id_usuario=usuario.id, status='pendente')
            db.session.add(novo_evento)

        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('criar_tarefa.html', form=formulario, usuarios=usuarios)

@app.route('/editar_tarefa/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):

    # Selecionar tarefa no banco de dados
    tarefa_atual = Tarefa.query.get(id)

    novoFormulario = FormularioEditarTarefa(status=tarefa_atual.status)

    if novoFormulario.validate_on_submit():
        novoFormulario.populate_obj(tarefa_atual)

        # Atualizar os valores da tarefa
        upt = update(Tarefa).values(
            nome_tarefa=novoFormulario.nome_tarefa.data,
            data_tarefa=novoFormulario.data_tarefa.data,
            descricao=novoFormulario.descricao.data,
            status=novoFormulario.status.data,
            id_usuario=tarefa_atual.id_usuario,
        ).where(Tarefa.id == id)

        db.session.execute(upt)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('editar_tarefa.html', form=novoFormulario, evento=tarefa_atual)

@app.route('/deletar_tarefa/<int:id>', methods=['GET', 'POST'])
def deletar_tarefa(id):
    tarefa_requerida = Tarefa.query.filter_by(id=id).first()

    if tarefa_requerida :
        db.session.delete(tarefa_requerida)
        db.session.commit()
        flash('Tarefa excluída com sucesso!', 'success')

    return redirect(url_for('dashboard'))

def iniciar():
    from banco import criar_banco
    with app.app_context():
        # Tentar criar o banco de dados
        criar_banco()

        existing_admin = Usuario.query.filter_by(is_admin=True).first()

        if not existing_admin:
            admin = Usuario(nome='admin', email=None, senha=generate_password_hash('admin'), is_admin=True)
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    iniciar()
    app.run(debug = True)