from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ModeloBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    data_atualizacao = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())