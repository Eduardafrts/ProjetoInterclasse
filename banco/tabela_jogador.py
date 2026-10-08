from flask import flash
from sqlalchemy import select, func
from sqlalchemy.dialects.mssql.information_schema import columns
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session, Time


def select_todos():
    # 1 - Montar o select
    # join(Tabela que quero juntar, condiçao= chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2 - Executar o select
    # Usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    print(jogadores)

    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

print(select_quantidade_total())

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
        db_session.add(jogador)
        db_session.commit()
        flash("Jogador criado com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")

select_todos()