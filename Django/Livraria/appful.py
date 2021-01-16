from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from http_verbs_base import *


collection = [
    {
     'titulo': 'Guerra dos Tronos',
     'preco': 59.9,
     'autor': 'Geroge R. R. Martin'
    },
    {
     'titulo': 'Fúria dos Reis',
     'preco': 57.9,
     'autor': 'Geroge R. R. Martin'
    },
    {
     'titulo': 'Tormenta de Espadas',
     'preco': 68.9,
     'autor': 'Geroge R. R. Martin'
    }
]

app = Flask(__name__)
app.secret_key = 'Excalibur150'
api = Api(app)


class Collection(Resource):
    def get(self):
        return {'acervo': collection}


class Book(Resource):
    def get(self, title):
        return get_base(item_endpoint=' '.join(title.split('_')),
                        item_key='titulo', table_name='livros', item_name='Livro')

    def post(self, title):
        return post_base(item_endpoint=' '.join(title.split('_')), items=collection,
                         item_key='titulo', table_name='livros', item_name='Livro')

    def put(self, title):
        # parser = reqparse.RequestParser()
        # parser.add_argument()
        # book = parser.parse_args()
        return put_base(item_endpoint=' '.join(title.split('_')), item_key='titulo', table_name='livros')

    def delete(self, title):
        # global collection
        # collection = list(filter(lambda x: x['titulo'] != ' '.join(title.split('_')), collection))
        return delete_base(item_endpoint=' '.join(title.split('_')), item_key='titulo', table_name='livros')


class Costumer(Resource):

    def __init__(self):
        self.costumers_columns_names, self.costumers_columns_types = get_columns('clientes')
        self.mapping(self)

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
        return post_base(item_endpoint=name, items=self.cls.costumers, item_key='nome',
                         table_name='clientes', item_name='Cliente')

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
        return post_base(item_endpoint=name, items=self.cls.managers, item_key='nome',
                         table_name='administradores', item_name='Administrador')

    def put(self, name):
        return put_base(item_endpoint=name, item_key='nome', table_name='administradores')

    def delete(self, name):
        manager = delete_base(item_endpoint=name, item_key='nome', table_name='administradores')
        manager['nascimento'] = manager['nascimento'].isoformat() if costumer['nascimento'] is not None else None
        return manager


class Author(Resource):
    pass


class PublishingCompany(Resource):
    pass


api.add_resource(Collection, '/bookstore/collection')
api.add_resource(Book, '/bookstore/collection/<string:title>')
api.add_resource(Costumer, '/bookstore/costumer_session/<string:name>')
api.add_resource(Manager, '/bookstore/manager_session/<string:name>')

app.run(port=5000, debug=True)
