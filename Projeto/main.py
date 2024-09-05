from flask import Flask, render_template, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import redirect

from config import app, db
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
            flash('Login ou senha incorretos')

        if usuarioDB:
            senhaDigitada = formsLogin.senha.data
            senhaDB = usuarioDB.senha

            if check_password_hash(senhaDB, senhaDigitada):
                login_user(usuarioDB)
                login = True
                return redirect('dashboard')
            else:
                # pop up no site?
                login = False
                print('>> Login ou senha incorretos')
                flash('Login ou senha incorretos')
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

        usuarioExistente = Usuario.query.filter_by(nome=usuarioNome).first()
        if usuarioExistente:
            print('>> Usuario ja cadastrado')
        else:
            novo_usuario = Usuario(nome=usuarioNome, email=usuarioEmail, senha=usuarioSenha)
            db.session.add(novo_usuario)
            db.session.commit()
            print('>> Usuario registrado!')
            return redirect(url_for('index'))

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
    return render_template('dashboard.html', usuario=nomeUsuario, eventos=eventos)

@app.route('/criar_evento', methods=['GET', 'POST'])
def criar_evento():
    from forms import FormularioEvento
    print(f'ID: {current_user.id}')
    formulario = FormularioEvento()

    if formulario.validate_on_submit():
        nomeEvento = formulario.nome_evento.data
        dataEvento = formulario.data_evento.data
        descEvento = formulario.descricao.data
        status = False


        usuBanco = Usuario.query.filter_by(id=current_user.id).first()

        eventoBanco = Evento.query.filter_by(nome_evento=nomeEvento).first()

        print(f'-- {nomeEvento} -- {dataEvento} -- {descEvento}')

        if eventoBanco:
            print('Evento ja existente')
        else:
            novo_evento = Evento(nome_evento=nomeEvento, data_evento=dataEvento, descricao=descEvento, id_usuario=usuBanco.id, status=False)
            db.session.add(novo_evento)
            db.session.commit()
            print('Evento Criado')
            # redirecionar
            return redirect(url_for('dashboard'))

    return render_template('criarEvento.html', form=formulario)

@app.route('/editar_evento/<int:evento_id>', methods=['GET', 'POST'])
def editar_evento():
    pass

@app.route('/deletar_evento/<int:evento_id>', methods=['GET', 'POST'])
def deletar_evento():
    pass

if __name__ == '__main__':
    app.run(debug = True)