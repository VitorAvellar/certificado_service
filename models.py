from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Certificado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    curso = db.Column(db.String(100))
    data = db.Column(db.String(10))
