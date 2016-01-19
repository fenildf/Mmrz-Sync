#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    write = start_response(status, response_headers)
    write("first write message\n")
    write("second write message\n")

    return "return message"

port  = 2603
httpd = make_server('', port, application)
print "Serving HTTP on port {0}...".format(port)

httpd.serve_forever()

