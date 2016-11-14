#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template, request

@route('/')
def index():
    return "Hello, world!!!"

run(host='localhost', port=3516)