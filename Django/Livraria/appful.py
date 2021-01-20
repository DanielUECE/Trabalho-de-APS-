#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_restful import Api
from resources.models import *


app = Flask(__name__)
app.secret_key = ''
api = Api(app)

api.add_resource(Collection, '/bookstore/collection')
api.add_resource(Book, '/bookstore/collection/<string:title>')
api.add_resource(Costumer, '/bookstore/costumer_session/<string:name>')
api.add_resource(Manager, '/bookstore/manager_session/<string:name>')
api.add_resource(Author, '/bookstore/author_session/<string:name>')
api.add_resource(PublishingCompany, '/bookstore/publishing_companys/<string:name>')

app.run(port=5000, debug=True)
