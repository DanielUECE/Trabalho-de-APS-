from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from psycopg2 import connect, extras
from config import DB_INFO
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


class Book(Resource):
    def get(self, title):
        for c in collection:
            if c['titulo'] == ' '.join(title.split('_')):
                return c
        return {'titulo': ' '.join(title.split('_')),  'preco': None, 'autor': None}, 404

    def delete(self, title):
        global collection
        collection = list(filter(lambda x: x['titulo'] != ' '.join(title.split('_')), collection))
        return collection


class Collection(Resource):
    def get(self):
        return {'acervo': collection}

    def put(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument()
        # book = parser.parse_args()
        book = request.get_json()
        for c in collection:
            if c['titulo'] == book['titulo']:
                c.update(book)
                return book
        collection.append(book)
        return book

    def post(self):
        book = request.get_json()
        collection.append(book)
        return book, 201


class Costumer(Resource):

    def __init__(self):
        conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                       user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
        cur = conn.cursor(cursor_factory=extras.DictCursor)
        cur.execute('SELECT * FROM clientes')
        self.costumers_columns_names = [desc[0] for desc in cur.description]
        cur.execute("""select *
                       from information_schema.columns
                       where table_schema NOT IN ('information_schema', 'pg_catalog')
                       order by table_schema, table_name""")
        self.costumers_columns_types = []
        for ccn in self.costumers_columns_names:
            for row in cur:
                if row['table_name'] == 'clientes' and row['column_name'] == ccn:
                    self.costumers_columns_types.append(row['data_type'])
        conn.close()
        self.mapping(self)

    @classmethod
    def mapping(cls, self):
        self.cls = cls
        conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                       user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes')
        fetch_costumers = cur.fetchall()
        t = len(self.costumers_columns_names)
        cls.costumers = []
        for cos in fetch_costumers:
            cd = dict()
            for i in range(t):
                cd.update({self.costumers_columns_names[i]: cos[i]})
            cls.costumers.append(cd)
        conn.close()
        cls.costumerid_mapping = {cos['id']: cos for cos in cls.costumers}
        cls.costumername_mapping = {cos['nome']: cos for cos in cls.costumers}

    @classmethod
    def find_costumer_by_name(cls, costumername):

        return cls.costumername_mapping.get(costumername, None)

    @classmethod
    def find_costumer_by_id(cls, _id):

        return cls.costumerid_mapping.get(_id, None)

    def post(self, name):
        return post_base(item=name, items=self.cls.costumers, item_endpoint='nome',
                         table_name='clientes', item_name='Clientes')
        # costumer = request.get_json()
        # if costumer['nome'] != name:
        #     raise Exception("Dados incompatíveis com endpoint")
        # for cos in self.cls.costumers:
        #     if cos['nome'] == name:
        #         return {'mensagem': 'Cliente já cadastrado!'}, 400
        # self.cls.costumers.append(costumer)
        # conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
        #                user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
        # cur = conn.cursor()
        # keys = '('
        # values = '('
        # for k, v in costumer.items():
        #     keys += k.replace('\'', '\\''')
        #     keys += ', '
        #     if isinstance(v, str):
        #         values += '\'' + v + '\''
        #     else:
        #         values += str(v)
        #
        #     values += ', '
        # keys = keys[:-2] + ')'
        # values = values[:-2] + ')'
        # cur.execute('INSERT INTO clientes {} VALUES {}'.format(keys, values))
        # conn.commit()
        # conn.close()
        # return costumer, 201

    def get(self, name):
        costumer = next(iter(filter(lambda x: x['nome'] == name, self.cls.costumers)), name)
        costumer['nascimento'] = costumer['nascimento'].isoformat()
        return costumer


api.add_resource(Book, '/bookstore/collection/<string:title>')
api.add_resource(Collection, '/bookstore/collection')
api.add_resource(Costumer, '/bookstore/costumer_session/<string:name>')

app.run(port=5000, debug=True)
