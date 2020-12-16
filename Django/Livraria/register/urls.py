#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from register import views

urlpatterns = [
    url(r'^$', views),
]

