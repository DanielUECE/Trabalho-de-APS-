#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="avalon",
                                                                                        DB_PASS="roundtable",
                                                                                        DB_ADDR="localhost",
                                                                                        DB_NAME="Livraria")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
