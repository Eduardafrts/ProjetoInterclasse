from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Partida


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    partidas_sql = select(Partida)
    # 2 - Executar o select
    partidas = db_session.execute(partidas_sql).scalars().all()

    return partidas


def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total

print(select_quantidade_total())


def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
        db_session.add(partida_nova)
        db_session.commit()
        flash("Partida criada com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")