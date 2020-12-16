#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = Trues
DB_INFO = {'DB_USER': None, 'DB_PASS': None, 'DB_ADDR': None, 'DB_NAME': None}
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=None,
                                                                                        DB_PASS=None,
                                                                                        DB_ADDR=None,
                                                                                        DB_NAME=None)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
