from .base import db, ModeloBase


class Ingresso(ModeloBase):
    """Opcional — vale ponto extra se implementar compra de ingresso."""

    __tablename__ = "ingressos"

    # TODO ALUNO: FK sessao_id → sessoes.id//
    sessao_id = db.Column(db.Integer, db.ForeingKey("sessoes.id"), nullable=False)
    assento = db.Column(db.String(10), nullable=False)
    nome_comprador = db.Column(db.String(120), nullable=False)
    sessao = db.relationship("Sessao", back_populates="ingressos")
    # TODO ALUNO: relationship sessao//
