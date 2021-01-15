#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI, DB_INFO
import models as mod
import pandas as pd
from psycopg2 import connect


engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


def fill_tipos():
    add(mod.Tipo(id=1, tipo='Ficção'))
    add(mod.Tipo(id=2, tipo='Não-ficção'))
    add(mod.Tipo(id=3, tipo='Autoajuda'))
    add(mod.Tipo(id=4, tipo='Religiosidade'))
    add(mod.Tipo(id=5, tipo='Ficção histórica'))
    add(mod.Tipo(id=6, tipo='Poesia'))
    add(mod.Tipo(id=7, tipo='Didático'))
    add(mod.Tipo(id=8, tipo='Receita'))


def fill_generos():
    add(mod.Genero(id=1, genero='Aventura'))
    add(mod.Genero(id=2, genero='Romance'))
    add(mod.Genero(id=3, genero='Ficção científica'))
    add(mod.Genero(id=4, genero='Policial'))
    add(mod.Genero(id=5, genero='Humor'))
    add(mod.Genero(id=6, genero='Infanto-juvenil'))
    add(mod.Genero(id=7, genero='Fanstasia'))
    add(mod.Genero(id=8, genero='Suspense'))
    add(mod.Genero(id=9, genero='Terror'))


def fill_estados():
    add(mod.Estado(id=1, estado='Novo'))
    add(mod.Estado(id=2, estado='Semi-novo'))
    add(mod.Estado(id=3, estado='Usado'))


def fill_livros():
    add(mod.Livro(titulo='Sapiens - Um breve resumo da história da Humanidade',  # ano_publicacao_original=2011,
                  edicao=1,  # editora='LP&M',
                  editora_id=1, ano_publicacao_edicao=2015, autores=['Yuval Noah Harari'],
                  # idioma_original='Hebraico',
                  idioma='Português', tipo_id=2, generos_id=None, estado_id=1))
    add(mod.Livro(titulo='Homo Deus - Uma breve história do amanhã',  # ano_publicacao_original=2015,
                  edicao=1,  # editora='Companhia das Letras',
                  editora_id=2, ano_publicacao_edicao=2016, autores=['Yuval Noah Harari'],
                  # idioma_original='Hebraico',
                  idioma='Português', tipo_id=2, generos_id=None, estado_id=1))


def create_tables():
    mod.Base.metadata.create_all(engine)

    fill_livros()
    fill_estados()
    fill_generos()
    fill_tipos()


def drop_tables():
    mod.Base.metadata.drop_all(engine)


def recreate_tables():
    drop_tables()
    create_tables()


def add(row):
    session.add(row)
    session.commit()


def close_session():
    session.close()
    engine.dispose()


def simple_query(table, lim=0):
    if lim == 0:
        session.query(table).all()
    else:
        session.query(table).limit(lim).all()


def to_xml(name, base):
    file = '<?xml version="1.0" encoding="utf-8"?>\n'
    file += f'\t<{name}s>\n'
    for i, f in base.iterrows():
        file += f'\t\t<{name}>\n'
        for k, v in f.to_dict().items():
            file += f'\t\t\t<{k}>{v}<{k}>\n'
        file += f'\t\t<{name}>\n'
    file += f'\t<{name}s>\n'
    print(file)


recreate_tables()
close_session()
# conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'], user=DB_INFO['DB_USER'],
#                password=DB_INFO['DB_PASS'])
# df = pd.read_sql_query('select * from livros', con=conn)
#
# to_xml('Livro', df)
# conn.close()
