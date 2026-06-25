from .base import db, ModeloBase


class Filme(ModeloBase):
    __tablename__ = "filmes"

    titulo = db.Column(db.String(150), nullable=False)
    duracao_min = db.Column(db.Integer, nullable=False)
    classificacao = db.Column(db.String(5), nullable=False)
    sessoes = db.relationship("Sessao", back_populates="filme")
    # TODO ALUNO: duracao_min (Integer), classificacao (String 5)//
    # TODO ALUNO: relationship sessoes//

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.titulo).all()
