from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select

from database import *
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    # 1- Montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()

    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=len(times),
        total_partidas=0
    )


@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        print(f'nome:{nome}, numero_camisa:{numero_camisa}, posicao:{posicao}, time_id:{time_id}')
        if not nome or not numero_camisa or not posicao:
            flash('preencha a informação que falta', 'error')
            return render_template('jogadores.html')

        try:
            jogador_novo = Jogador(nome=nome, numero_camisa=numero_camisa, posicao=posicao)
            # Inicia sessao do banco de dados
            db_session.add(jogador_novo)
            db_session.commit()
            flash('Jogador adicionado com sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()  # Reverte a transaçao em caso de erro
            flash(f'erro ao salvar no banco: {e}', 'error')
            print(f'erro ao salvar no banco: {e}')
            # 1- Montar o select
    times_sql = select(Time)
     # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()


    return render_template("jogadores.html", jogadores=[], times=times)


@app.route("/times")
def listar_times():
    # 1- Montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    return render_template("times.html", times=times)



@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        #Pegar valores no form
        nome = request.form.get("nome", "").strip()
        turma =request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        print(f'nome:{nome}, turma:{turma}')
        #Verificar se foi digitado
        if not nome:
            flash('Preencha o nome', 'error')
            return render_template('times.html')
        if not turma:
            flash('Preencha a turma', 'error')
            return render_template('times.html')
        if not responsavel:
            flash('Preencha o responsável', 'error')
            return render_template('times.html')
        #Salvar no banco
        try:
            time_novo = Time(nome=nome, turma=turma, responsavel=responsavel)
            db_session.add(time_novo)
            db_session.commit()
            flash('Time adicionado com sucesso', 'success')
        except SQLAlchemyError as e:
            db_session.rollback()
            flash(f'erro ao salvar  no banco: {e}', 'error')
            print(f'erro ao salvar no banco: {e}')

        except Exception as e:
            db_session.rollback()
            flash(f'erro: {e}', 'error')
            print(f'erro: {e}')

# Buscar todos os times do banco -----------
    # 1- Montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    return render_template("times.html", times=times)





@app.route("/partidas")
def listar_partidas():

    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        placar_casa = request.form.get("placar_casa") or 0
        placar_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        print(time_casa_id, time_visitante_id, placar_casa, placar_visitante, data_partida=data_partida)
    return render_template("partidas.html", partidas=[], times=[])


if __name__ == "__main__":
    app.run(debug=True)
