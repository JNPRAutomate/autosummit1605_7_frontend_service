#!/usr/bin/python
from docker import Client
import argparse
import influxdb
import docker.tls as tls
from os import path
import os
import pprint
import subprocess
import json
import os.path
from sys import platform as _platform
import requests
import cherrypy
import multiprocessing.pool
from threading import Thread
from flask import *
import math
import time
import sys
import yaml
from jinja2 import Template
from jnpr.junos import Device
from jnpr.junos.exception import RpcError
from jnpr.junos.utils.config import Config as junos_config
from jnpr.junos.factory.factory_loader import FactoryLoader


dport = ''
parser = argparse.ArgumentParser(add_help=True)

parser.add_argument("-p", action="store",
                    help="Destination Port - Range 1-65535", required=True)

args = parser.parse_args()

if args.p:
    dport = int(args.p)
    if dport > 65535 or args.p < 1:
        print "Please select a TCP Port between 1-65535"
        parser.print_help()
        sys.exit()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/infra', methods=['GET', 'POST'])
def infra():
    return render_template('infra.html')

@app.route('/prvsn', methods=['GET', 'POST'])
def prvsn():
    return render_template('prvsn.html')

@app.route('/provision_services', methods=['GET', 'POST'])
def provision_services():
    customername = request.form.get('customername')
    service1 = request.form.get('service1')
    service2 = request.form.get('service2')
    service3 = request.form.get('service3')
    service4 = request.form.get('service4')
    service5 = request.form.get('service5')
    campus = request.form.get('campus')
    internet = request.form.get('internet')
    legacy = request.form.get('legacy')
    provisioned_services = ''
    provisioned_services += Markup('''\
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body><center>
Provisioned - <br>''')
    if service1:
        provisioned_services += Markup('''Service 1<br>''')

    if service2:
        provisioned_services += Markup('''Service 2<br>''')

    if service3:
        provisioned_services += Markup('''Service 3<br>''')

    if service4:
        provisioned_services += Markup('''Service 4<br>''')

    if service5:
        provisioned_services += Markup('''Service 5<br>''')

    if campus:
        provisioned_services += Markup('''Campus<br>''')

    if internet:
        provisioned_services += Markup('''Internet<br>''')

    if legacy:
        provisioned_services += Markup('''Legacy<br>''')

    provisioned_services += Markup('''<button type="button" name="button" class="btn btn-primary btn-lg" onClick="location.href='../'" enabled><strong>Return to Main Page</strong></button><br>''')
    provisioned_services += Markup('''</body></html>''')
    print provisioned_services
    return render_template('success.html', info=provisioned_services)

def run_web_server():
    global dport
    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = dport
    server.thread_pool = 30
    server.ssl_module            = 'pyopenssl'
    server.ssl_certificate       = 'server.crt'
    server.ssl_private_key       = 'server.key'
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

t1 = Thread(target = run_web_server)
t1.start()
