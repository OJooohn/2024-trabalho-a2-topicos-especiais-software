from flask import Flask, render_template, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import redirect

from config import app, db
from modelosBanco import *

@app.route('/', methods=['GET', 'POST'])
def index():
    from forms import FormularioLogin
    from werkzeug.security import check_password_hash

    formsLogin = FormularioLogin()

    if formsLogin.validate_on_submit():
        usuarioNome = formsLogin.nome.data
        usuarioDB = Usuario.query.filter_by(nome=usuarioNome).first()
        print(usuarioDB)

        if usuarioDB:
            senhaDigitada = formsLogin.senha.data
            senhaDB = usuarioDB.senha

            if check_password_hash(senhaDB, senhaDigitada):
                print(f'>> Usuario: {usuarioNome}')
                login_user(usuarioDB)
                return redirect('dashboard')
            else:
                # pop up no site?
                print('>> Login ou senha incorretos')
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

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug = True)