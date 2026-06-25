from flask_sqlalchemy import SQLAlchemy
from . import  __all__

db = SQLAlchemy()

class ModeloBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column()
    data_atualizacao = db.Column()