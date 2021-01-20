#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
DB_INFO = {'user': None, 'password': None, 'host': None, 'database': None}
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}/{database}".format(**DB_INFO)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
