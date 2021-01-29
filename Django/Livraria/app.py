#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_restful import Api
from resources.resources import *
from json import loads, dumps


ADDRESS_ATTRIBUTES = ['estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento']


def endereco(data):
    endereco = dict()
    for aa in ADDRESS_ATTRIBUTES:
        endereco.update({aa: data[aa]})
        del data[aa]
    data['endereco'] = dumps(endereco)
    return data


app = Flask(__name__)
app.secret_key = ''
api = Api(app)

api.add_resource(Collection, '/bookstore/collection')
api.add_resource(Book, '/bookstore/collection/<string:title>')
api.add_resource(Costumer, '/bookstore/costumer_session/<string:name>')
api.add_resource(Manager, '/bookstore/manager_session/<string:name>')
api.add_resource(Author, '/bookstore/author_session/<string:name>')
api.add_resource(PublishingCompany, '/bookstore/publishing_companys/<string:name>')


@app.route('/bookstore')
def home():
    return render_template('index.html')


@app.route('/bookstore/costumer_register')
def render_costumer_register():
    return render_template('inscrevase.html')


@app.route('/bookstore/costumer_session/<string:name>')
def render_costumer():
    return render_template('')


@app.route('/bookstore/costumer_register', methods=['GET', 'POST'])
def costumer_register():
    data = loads(dumps(request.form))
    if data['senha'] == data['confirma-senha']:
        del data['confirma-senha']
        del data['btnCadastrar']
        data = endereco(data)
        costumer = Costumer(data)
        costumer.post(data['nome'])
    else:
        print("Senha incorreta")


@app.route('/bookstore/collection')
def render_collection():
    return render_template('')


@app.route('/bookstore/collection/register')
def render_book_register():
    # conn = connect(**DB_INFO)
    # cur = conn.cursor()
    # cur.execute('select * from editoras')
    # editoras = cur.fetchall()
    editoras, _, _ = mapping_base('editoras')
    # conn.close()
    return render_template('cadastrar_livro.html', editoras=editoras)


@app.route('/bookstore/collection/register', methods=['GET', 'POST'])
def book_register():
    data = loads(dumps(request.form))
    del data['btnCadastrar_livro']
    data['autores'] = [data['autor']]
    del data['autor']
    del data['categoria']
    data['tipo_id'] = 1
    data['estado_id'] = 1
    data['classificacao'] = 0.0
    print(data)
    book = Book(data)
    book.post(data['titulo'])


@app.route('/bookstore/publishing_company_register')
def render_publishing_company_register():
    return render_template('inserir_editoras.html')


@app.route('/bookstore/publishing_company_register', methods=['POST'])
def publishing_company_register():
    data = loads(dumps(request.form))
    data = endereco(data)
    del data['btnInserir_Editora']
    pc = PublishingCompany(data)
    pc.post(data['nome'])


@app.route('/bookstore/collection/<string:title>')
def render_book(title):
    livros, _, _ = mapping_base('livros')
    titulo = ' '.join(title.split('_'))
    livro = next(iter((filter(lambda x: x['titulo'] == titulo, livros))))
    print(livro)
    if len(livro) == 1:
        livro['autor'] = livro['autores'][0] + ', '
    else:
        autores = ''
        for l in livro['autores']:
            autores += l + ', '
        livro['autor'] = autores[:-2]
    del livro['autores']
    return render_template('livro_template.html', livro=livro)


app.run(port=5000, debug=True)
