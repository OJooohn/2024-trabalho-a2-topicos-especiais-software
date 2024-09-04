from config import app, db
from modelosBanco import Usuario, Evento

with app.app_context():
    db.create_all()  # precisa de um contexto

