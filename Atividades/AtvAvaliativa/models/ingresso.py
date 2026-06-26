from .base import db, ModeloBase


class Ingresso(ModeloBase):
    __tablename__ = "ingressos"

    assento = db.Column(db.String(10), nullable=False)
    nome_comprador = db.Column(db.String(120), nullable=False)

    sessao_id = db.Column(
        db.Integer,
        db.ForeignKey("sessoes.id"),
        nullable=False
    )

    sessao = db.relationship("Sessao", back_populates="ingressos")