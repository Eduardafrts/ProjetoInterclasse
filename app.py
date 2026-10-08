# Bibliotecas --------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from banco import tabela_time, tabela_jogador, tabela_partida
from database import *
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()


    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,
    )


@app.route("/jogadores")
def listar_jogadores():

    jogadores = tabela_jogador.select_todos()
    print(jogadores)
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    # Quando clicar no botão cadastrar
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome").strip()
        numero_camisa = request.form.get("camisanumero") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # 2 - Verificar se foi digitado
        if not nome:
            flash("Preencha o nome", "error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("Preencha a turma", "error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("Preencha a posição", "error")
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash("Preencha o time", "error")
            return redirect(url_for("novo_jogador"))

        # 3 - Salvar no banco
        tabela_jogador.salvar(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    # Select times para escolher no formulario
    #   Buscar todos os times no banco
    times = tabela_time.select_todos()
  #   Buscar todos os jogadores no banco
    jogadores = tabela_jogador.select_todos()

    # Carregar o formulario
    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)



@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome")
        turma = request.form.get("turma")
        responsavel = request.form.get("responsavel")

        # 2 - Verificar se foi digitado
        if not nome:
            flash("Preencha o nome", "error")
            return redirect(url_for("novo_time"))
        if not turma:
            flash("Preencha a turma", "error")
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash("Preencha o responsável", "error")
            return redirect(url_for("novo_time"))

        # 3 - Salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)



@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    return render_template("partidas.html", partidas=partidas)

@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        # 1 - pegar os campos do formulario
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # 2 - Verificar se foi digitado
        if not time_casa_id:
            flash("Preencha o time_casa", "error")
            return redirect(url_for("nova_partida"))
        if not time_visitante_id:
            flash("Preencha o time_visitante_id", "error")
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash("Preencha o gols_casa", "error")
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash("Preencha o gols_visitante", "error")
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash("Preencha o data_partida", "error")
            return redirect(url_for("nova_partida"))

        # 3 - Verificar se os times são iguais
        if time_casa_id == time_visitante_id:
            flash("Selecione times diferentes ", "error")
            return render_template("partidas.html")

        # 4 - Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa,
        gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
