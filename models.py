from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Certificado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(14))
    nacionalidade = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    curso = db.Column(db.String(100))
    data = db.Column(db.String(10))
