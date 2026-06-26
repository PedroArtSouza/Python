from flask import Blueprint, redirect, render_template, request, url_for
from datetime import datetime 
from models import Filme, Sala, Sessao, db

# Blueprint = módulo de rotas do cinema (registrar no app.py com register_blueprint)
cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@cinema_bp.route("/")
def index():
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)

@cinema_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        filme_id = request.form.get("filme_id")
        sala_id = request.form.get("sala_id")
        data_hora_string = request.form.get("data_hora")
        preco = request.form.get("preco")

        nova_sessao = Sessao(
            filme_id=filme_id,
            sala_id=sala_id,
            data_hora=data_hora_string, # Troque para data_hora_obj se necessário
            preco=preco,
        )
        
        db.session.add(nova_sessao)
        db.session.commit()
        
        return redirect(url_for("cinema.index"))

    return render_template(
        "cinema/formulario_sessao.html",
        filmes=filmes,
        salas=salas,
    )