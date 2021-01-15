#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api

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


@app.route('/')
def home():
    return render_template('index_example.html')

# POST /bookstore/collection/<string:title> {'titulo': , 'preco':, 'autor': }
@app.route('/bookstore/collection/<string:title>', methods=['POST'])


# POST /bookstore/collection {'livro': ,}
@app.route('/bookstore/collection', methods=['POST'])
def add_book_to_collection():
    requested_book = request.get_json()
    collection.append(requested_book)
    return jsonify(requested_book)

# GET /bookstore/collection/<string:title> {'titulo': , 'preco':, 'autor': }
@app.route('/bookstore/collection/<string:title>')
def get_book(title):
    for c in collection:
        if c['titulo'] == ' '.join(title.split('_')):
            return jsonify(c)
    return jsonify({'message': 'Livro não encontrado'})


# GET /bookstore/collection {'livro': ,}
@app.route('/bookstore/collection')
def get_collection():
    return jsonify({'acervo': collection})


app.run(port=5000)
