#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric, PrimaryKeyConstraint, ARRAY, DATE

Base = declarative_base()


class Livro(Base):

    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    ano_publicacao_original = Column(Numeric, nullable=False)
    edicao = Column(Numeric, nullable=False)
    editora = Column(String, nullable=False)
    ano_publicacao_edicao = Column(Numeric, nullable=False)
    autores = Column(ARRAY(String), nullable=False)
    lingua_original = Column(String, nullable=False)
    lingua = Column(String, nullable=False)
    tipo_id = Column(Numeric, nullable=False)
    generos_id = Column(ARRAY(Numeric))
    estado_id = Column(Numeric, nullable=False)
    exemplares = Column(Numeric, default=0)
    preco = Column(Numeric(3, 2))
    paginas = Column(Numeric)
    classificao = Column(Numeric)


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Numeric, nullable=False)
    nome = Column(String, nullable=False)
    nascimento = Column(DATE, nullable=False)
    cidade = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tipo = Column(Numeric, nullable=False)


class Tipo(Base):
    __tablename__ = 'tipos'

    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)


class Genero(Base):

    __tablename__ = 'generos'

    id = Column(Integer, primary_key=True)
    genero = Column(String, nullable=False)


class Estado(Base):

    __tablename__ = 'estados'

    id = Column(Integer, primary_key=True)
    estado = Column(String, nullable=False)
