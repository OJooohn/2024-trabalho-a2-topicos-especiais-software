from config import app, db

# precisa para criar o banco certo
from modelosBanco import Usuario, Tarefa

with app.app_context():
    db.create_all()