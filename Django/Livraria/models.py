#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, PrimaryKeyConstraint
from sqlalchemy import ARRAY, DATE, PickleType, JSON, LargeBinary, TEXT
from sqlalchemy.orm import relationship

Base = declarative_base()


class Livro(Base):

    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    ano_publicacao_original = Column(Integer, nullable=False)
    edicao = Column(Integer, nullable=False)
    editora_id = Column(Integer, ForeignKey('editoras.id'), nullable=False)
    ano_publicacao_edicao = Column(Integer, nullable=False)
    autores = Column(ARRAY(String), nullable=False)
    # idioma_original = Column(String, nullable=False)
    idioma = Column(String, nullable=False)
    tipo_id = Column(Integer, nullable=False)
    generos_id = Column(ARRAY(Integer))
    categoria_id = Column(Integer)
    estado_id = Column(Integer, nullable=False)
    exemplares = Column(Integer, default=0)
    preco = Column(Numeric(6, 2))
    paginas = Column(Integer)
    classificacao = Column(Numeric, default=0.0, nullable=False)
    capa = Column(LargeBinary, nullable=False)
    capa_extra1 = Column(LargeBinary)
    capa_extra2 = Column(LargeBinary)
    sinopse = Column(TEXT)

    # Relationships

    # editora = relationship('Editora')
    # tipo = relationship('Tipo')
    # categoria = relationship('Categoria')
    # estado = relationship('Estado')


class Editora(Base):

    __tablename__ = 'editoras'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(JSON, nullable=False)


class Autor(Base):

    __tablename__ = 'autores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)


class Cliente(Base):

    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(DATE, nullable=False)
    endereco = Column(JSON, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    visualizados = Column(ARRAY(Integer))


class Administrador(Base):

    __tablename__ = 'administradores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(DATE, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False)


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


class Categoria(Base):

    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    categoria = Column(String, nullable=False)


class Status(Base):

    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
