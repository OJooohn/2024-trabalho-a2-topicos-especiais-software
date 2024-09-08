from config import app, db

# É necessário para criar o banco de dados com as tabelas Usuario e Tarefa
# Apenas criamos outro arquivo para fins de organização de código
from modelosBanco import Usuario, Tarefa

with app.app_context():
    db.create_all()