#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse

from http_verbs_base import *


class Collection(Resource):
    def get(self):
        conn = connect(**DB_INFO)
        df = pd.read_sql('SELECT * FROM livros', con=conn)
        collection = list(df.where(pd.notnull(df), None).to_dict('index').values())
        conn.close()
        return {'acervo': collection}


class Book(Resource):

    def __init__(self, data=None):
        self.data = data

    # def get(self, title):
    #     return get_base(item_endpoint=' '.join(title.split('_')),
    #                     item_key='titulo', table_name='livros', item_name='Livro')

    def post(self, title):
        return post_base(item_endpoint=' '.join(title.split('_')), item_key='titulo',
                         table_name='livros', item_name='Livro', data=self.data)

    def put(self, title):
        return put_base(item_endpoint=' '.join(title.split('_')), item_key='titulo', table_name='livros')

    def delete(self, title):
        # global collection
        # collection = list(filter(lambda x: x['titulo'] != ' '.join(title.split('_')), collection))
        return delete_base(item_endpoint=' '.join(title.split('_')), item_key='titulo', table_name='livros')


class Costumer(Resource):

    def __init__(self, data=None):
        self.costumers_columns_names, self.costumers_columns_types = get_columns('clientes')
        self.mapping(self)
        self.data = data

    @classmethod
    def mapping(cls, self):
        self.cls = cls

        cls.costumers, cls.costumerid_mapping, cls.costumername_mapping = mapping_base('clientes',
                                                                                       self.costumers_columns_names)

    @classmethod
    def find_costumer_by_name(cls, costumername):

        return cls.costumername_mapping.get(costumername, None)

    @classmethod
    def find_costumer_by_id(cls, _id):

        return cls.costumerid_mapping.get(_id, None)

    def get(self, name):
        # self.mapping(self)
        # costumer = next(iter(filter(lambda x: x['nome'] == name, self.cls.costumers)), name)
        costumer, http_code = get_base(item_endpoint=name, item_key='nome', table_name='clientes', item_name='Cliente')
        costumer['nascimento'] = costumer['nascimento'].isoformat()
        return costumer, http_code

    def post(self, name):
        return post_base(item_endpoint=name, item_key='nome', table_name='clientes',
                         item_name='Cliente', data=self.data)

    def put(self, name):
        return put_base(item_endpoint=name, item_key='nome', table_name='clientes')

    def delete(self, name):
        costumer = delete_base(item_endpoint=name, item_key='nome', table_name='clientes')
        costumer['nascimento'] = costumer['nascimento'].isoformat() if costumer['nascimento'] is not None else None
        return costumer


class Manager(Resource):
    def __init__(self):
        self.managers_columns_names, self.managers_columns_types = get_columns('clientes')
        self.mapping(self)

    @classmethod
    def mapping(cls, self):
        self.cls = cls

        cls.managers, cls.managerid_mapping, cls.managername_mapping = mapping_base('clientes',
                                                                                       self.managers_columns_names)

    def get(self, name):
        return get_base(item_endpoint=name, item_key='nome',
                        table_name='administradores', item_name='Administrador')

    def post(self, name):
        return post_base(item_endpoint=name, item_key='nome',
                         table_name='autores', item_name='Autor')

    def put(self, name):
        return put_base(item_endpoint=name, item_key='nome', table_name='autores')

    def delete(self, name):
        return delete_base(item_endpoint=name, item_key='nome', table_name='autores')


class Author(Resource):

    def __init__(self, data):
        self.data = data

    def get(self, name):
        return get_base(item_endpoint=name, item_key='nome',
                        table_name='autores', item_name='Autor')

    def post(self, name):
        return post_base(item_endpoint=name, item_key='nome',
                         table_name='autores', item_name='Autor', data=self.data)

    def put(self, name):
        return put_base(item_endpoint=name, item_key='nome', table_name='autores')

    def delete(self, name):
        return delete_base(item_endpoint=name, item_key='nome', table_name='autores')


class PublishingCompany(Resource):

    def __init__(self, data):
        self.data = data

    def get(self, name):
        return get_base(item_endpoint=name, item_key='nome',
                        table_name='editoras', item_name='Editora')

    def post(self, name):
        return post_base(item_endpoint=name, item_key='nome',
                         table_name='editoras', item_name='Editora', data=self.data)

    def put(self, name):
        return put_base(item_endpoint=name, item_key='nome', table_name='editoras')

    def delete(self, name):
        return delete_base(item_endpoint=name, item_key='nome', table_name='editoras')

