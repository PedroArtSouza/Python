from . import db
from .base import ModeloBase


class Sala(ModeloBase):
    __tablename__ = "salas"

    numero = db.Column(db.Integer, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    sessoes = db.relationship("Sessao", back_populates="salas")
    # TODO ALUNO: relationship sessoes//

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.numero).all()
