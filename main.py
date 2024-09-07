from xml.etree.ElementTree import tostring

from flask import Flask, render_template, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import update
from werkzeug.utils import redirect

from config import app, db
from forms import FormularioEvento, FormularioEditarEvento, FormularioAtualizarEvento
from modelosBanco import *

@app.route('/', methods=['GET', 'POST'])
def index():
    from forms import FormularioLogin
    from werkzeug.security import check_password_hash

    login = None

    formsLogin = FormularioLogin()

    if formsLogin.validate_on_submit():
        usuarioNome = formsLogin.nome.data
        usuarioDB = Usuario.query.filter_by(nome=usuarioNome).first()

        print(f'>> Nome: {usuarioNome} >> UserDB: {usuarioDB}')

        if usuarioDB is None:
            print(f'Login: {login}')
            print('>> Login ou senha incorretos')
            flash(f'Usuário "{ usuarioNome }" não encontrado. Tente novamente')

        if usuarioDB:
            senhaDigitada = formsLogin.senha.data
            senhaDB = usuarioDB.senha

            if check_password_hash(senhaDB, senhaDigitada):
                login_user(usuarioDB)
                login = True
                return redirect('dashboard')
            else:
                print('>> Login ou senha incorretos')
                flash('Senha incorreta... Digite novamente')
                return redirect(url_for('index'))

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

        print(f'Usuario: {usuarioNome} | Senha codificada: {usuarioSenha}')

        if formsRegistro.senha.data == formsRegistro.confirmar_senha.data:
            usuarioExistente = Usuario.query.filter_by(nome=usuarioNome).first()
            emailExistente = Usuario.query.filter_by(email=usuarioEmail).first()
            if usuarioExistente:
                print('>> Usuario ja cadastrado')
                flash('Usuario ja cadastrado. Escolha outro nome de usuário!')
            elif emailExistente:
                print('>> Usuario ja cadastrado')
                flash('Email ja cadastrado. Digite outro email!')
            else:
                novo_usuario = Usuario(nome=usuarioNome, email=usuarioEmail, senha=usuarioSenha)
                db.session.add(novo_usuario)
                db.session.commit()
                print('>> Usuario registrado!')
                return redirect(url_for('index'))
        else:
            flash('Por favor, confirme a senha corretamente')
            return redirect(url_for('register'))

    return render_template('register.html', form=formsRegistro)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    nomeUsuario = current_user.nome
    eventos = Evento.query.filter_by(id_usuario=current_user.id).all()
    return render_template('dashboard.html', eventos=eventos, usuario=nomeUsuario)

@app.route('/criar_evento', methods=['GET', 'POST'])
def criar_evento():
    # Usuarios que não são o usuário logado
    # Aparecem na lista de seleção
    usuarios = Usuario.query.filter(Usuario.id != current_user.id).all()

    # Criando uma tupla com os usuários para a criação dos eventos
    usuarios_escolhidos = [(user.id, user.nome) for user in usuarios]

    # Passando a tupla para o formulário
    formulario = FormularioEvento(user_choices=usuarios_escolhidos)

    if formulario.validate_on_submit():

        # Pegar os dados do formulário
        nomeEvento = formulario.nome_evento.data
        dataEvento = formulario.data_evento.data
        descEvento = formulario.descricao.data

        usuBanco = Usuario.query.filter_by(id=current_user.id).first()

        eventoBanco = Evento.query.filter_by(nome_evento=nomeEvento).first()

        print(f'-- {nomeEvento} -- {dataEvento} -- {descEvento}')

        if eventoBanco:
            print('Evento ja existente')
        else:
            novo_evento = Evento(nome_evento=nomeEvento, data_evento=dataEvento, descricao=descEvento, id_usuario=usuBanco.id, status='pendente')
            db.session.add(novo_evento)
            db.session.commit()

            # Adicionar usuários selecionados ao evento
            for usuario_selecionado in formulario.usuarios.data:
                usuario = Usuario.query.get(usuario_selecionado)
                novo_evento = Evento(nome_evento=nomeEvento, data_evento=dataEvento, descricao=descEvento, id_usuario=usuario.id, status='pendente')
                db.session.add(novo_evento)
            db.session.commit()

            print('Evento Criado')
            return redirect(url_for('dashboard'))

    return render_template('criarEvento.html', form=formulario, usuarios=usuarios)

@app.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):

    evento_atual = Evento.query.get(id)
    nome_evento = evento_atual.nome_evento
    data_evento = evento_atual.data_evento
    descricao = evento_atual.descricao
    status = evento_atual.status

    print(f'Desc: {descricao}')
    print(f'Status: {status}')
    print(f'Tipo nome: {type(descricao)}')
    print(f'Tipo status: {type(status)}')

    novoFormulario = FormularioEditarEvento(status=evento_atual.status)

    if novoFormulario.validate_on_submit():
        novoFormulario.populate_obj(evento_atual)

        upt = update(Evento).values(
            nome_evento=novoFormulario.nome_evento.data,
            data_evento=novoFormulario.data_evento.data,
            descricao=novoFormulario.descricao.data,
            status=novoFormulario.status.data,
            id_usuario=evento_atual.id_usuario,
        ).where(Evento.id == id)

        db.session.execute(upt)
        db.session.commit()

        print(f'Atualizado -- Nome: {novoFormulario.nome_evento.data}')
        print(f'Atualizado -- Data: {novoFormulario.data_evento.data}')
        print(f'Atualizado -- Descricao: {novoFormulario.descricao.data}')
        print(f'Atualizado -- Status: {novoFormulario.status.data}')
        return redirect(url_for('dashboard'))

    return render_template('editarEvento.html', form=novoFormulario, evento=evento_atual)

@app.route('/deletar_evento/<int:id>', methods=['GET', 'POST'])
def deletar_evento(id):
    evento_requerido = Evento.query.filter_by(id=id).first()

    if evento_requerido is None:
        print('Evento não encontrado')
        return redirect(url_for('dashboard'))
    else:
        db.session.delete(evento_requerido)
        db.session.commit()
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug = True)