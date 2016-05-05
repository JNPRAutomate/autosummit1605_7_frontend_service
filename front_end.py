#!/usr/bin/python
import argparse
import influxdb
import docker.tls as tls
import os
import pprint
import subprocess
import json
import os.path
import requests
import cherrypy
import multiprocessing.pool
import math
import time
import sys
import yaml
from docker import Client
from sys import platform as _platform
from threading import Thread
from flask import *
from os import path
from jinja2 import Template
from jnpr.junos import Device
from jnpr.junos.exception import RpcError
from jnpr.junos.utils.config import Config
from jnpr.junos.factory.factory_loader import FactoryLoader

JinjaTemplate_Campus = Template("""
security {
  zones {
    security-zone DC {
      address-book {
        address {{ var1 }} {{ Address }}/32;
        address-set CAMPUS_USER {
          address {{ var1 }};
        }
      }
    }
  }
}""")

JinjaTemplate_Internet = Template("""
security {
  zones {
    security-zone DC {
      address-book {
        address {{ var1 }} {{ Address }}/32;
        address-set INTERNET_USER {
          address {{ var1 }};
        }
      }
    }
  }
}""")

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
    name = request.form.get('name')
    ip_address = request.form.get('ip_address')
    campus_user = request.form.get('campus_user')
    service2 = request.form.get('service2')
    service3 = request.form.get('service3')
    service4 = request.form.get('service4')
    service5 = request.form.get('service5')
    campus = request.form.get('campus')
    internet_user = request.form.get('internet_user')
    legacy = request.form.get('legacy')
    provisioned_services = ''
    provisioned_services += Markup('''\
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body><center>
Provisioned - <br>''')

    if campus_user:
        dev = Device(host='172.25.45.68', user='lab', passwd='jnpr123')
        cu = Config(dev)
        print name, ip_address
        try:
            dev.open()
            dev.timeout = 300
            cu.lock()
            jinja_input = {'Address': ip_address, 'var1': name}
            jinja_data = open("jinjafile.conf", "wb")
            jinja_data.write(JinjaTemplate_Campus.render(**jinja_input))
            jinja_data.close()
            rsp = cu.load( template_path="jinjafile.conf", merge=True )
            cu.commit()
            cu.unlock()

        except RpcError:
            msg = "{0} was Skipped due to RPC Error.  Device is not a Juniper SRX Series"
            print msg
            dev.close()

        except Exception as err:
            msg = "{0} was skipped due to unhandled exception.\n{1}"
            print msg
            traceback.print_exc(file=sys.stdout)

        dev.close()

        provisioned_services += Markup('''Campus User: '''+name+''' with IP Address:'''+ip_address+'''<br>''')

    if internet_user:
        dev = Device(host='172.25.45.68', user='lab', passwd='jnpr123')
        cu = Config(dev)
        print name, ip_address
        try:
            dev.open()
            dev.timeout = 300
            cu.lock()
            jinja_input = {'Address': ip_address, 'var1': name}
            jinja_data = open("jinjafile.conf", "wb")
            jinja_data.write(JinjaTemplate_Internet.render(**jinja_input))
            jinja_data.close()
            rsp = cu.load( template_path="jinjafile.conf", merge=True )
            cu.commit()
            cu.unlock()

        except RpcError:
            msg = "{0} was Skipped due to RPC Error.  Device is not a Juniper SRX Series"
            print msg
            dev.close()

        except Exception as err:
            msg = "{0} was skipped due to unhandled exception.\n{1}"
            print msg
            traceback.print_exc(file=sys.stdout)

        dev.close()

        provisioned_services += Markup('''Internet User'''+name+''' with IP Address: '''+ip_address+'''<br>''')

    if legacy:
        provisioned_services += Markup('''Legacy<br>''')

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

    provisioned_services += Markup('''<button type="button" name="button" class="btn btn-primary btn-lg" onClick="location.href='../'" enabled><strong>Return to Main Page</strong></button><br>''')
    provisioned_services += Markup('''</body></html>''')
    print provisioned_services
    return render_template('success.html', info=provisioned_services)

@app.route('/leaf5_on')
def leaf5_on():
    os.system("virsh start t1_leaf5")
    os.system("virsh start t1_leaf5_child")
    return render_template('index.html')

@app.route('/leaf5_off')
def leaf5_off():
    os.system("virsh destroy t1_leaf5")
    os.system("virsh destory t1_leaf5_child")
    return render_template('index.html')

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
