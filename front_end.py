#!/usr/bin/python
import cherrypy
import multiprocessing.pool
from threading import Thread
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from gevent import pywsgi, sleep
from socketio.namespace import BaseNamespace
from gevent import server
from gevent.server import _tcp_listener
from gevent import monkey; monkey.patch_all()
from flask import *
import math
import time
import sys

app = Flask(__name__)

@app.route('/')
def index():
    build_index_html = open("./templates/index.html", "wb")
    process_index_html  = Markup('''\
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta charset="utf-8" />
        <title>Automation Toolset</title>
        <link rel="stylesheet" href="">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js" type="text/javascript"></script>
        <script type="text/javascript">
        $(document).ready(function(){
            $('#button1').on('click', function(){
                if($("a").hasClass("on")){
                    $.ajax({
                        type: 'POST',
                        url: '/action1_on',
                    });
                    $(this).toggleClass('on');
                }
                else{
                    $.ajax({
                        type: 'POST',
                        url: '/action1_off',
                    });
                    $(this).toggleClass('on');
                }
            });
        });
        </script>
        <script type="text/javascript">
        $(document).ready(function(){
            $('#button2').on('click', function(){
                if($("b").hasClass("on")){
                    $.ajax({
                        type: 'POST',
                        url: '/action2_on',
                    });
                    $(this).toggleClass('on');
                }
                else{
                    $.ajax({
                        type: 'POST',
                        url: '/action2_off',
                    });
                    $(this).toggleClass('on');
                }
            });
        });
        </script>
        <script type="text/javascript">
        $(document).ready(function(){
            $('#button3').on('click', function(){
                if($("c").hasClass("on")){
                    $.ajax({
                        type: 'POST',
                        url: '/action3_on',
                    });
                    $(this).toggleClass('on');
                }
                else{
                    $.ajax({
                        type: 'POST',
                        url: '/action3_off',
                    });
                    $(this).toggleClass('on');
                }
            });
        });
        </script>
        <script type="text/javascript">
        $(document).ready(function(){
            $('#button4').on('click', function(){
                if($("d").hasClass("on")){
                    $.ajax({
                        type: 'POST',
                        url: '/action4_on',
                    });
                    $(this).toggleClass('on');
                }
                else{
                    $.ajax({
                        type: 'POST',
                        url: '/action4_off',
                    });
                    $(this).toggleClass('on');
                }
            });
        });
        </script>
</head>
<style>
h1 {
  background-image: url('/static/micro_carbon.png');
  font-family: "Avant Garde", Avantgarde, "Century Gothic", CenturyGothic, "AppleGothic", sans-serif;
  font-size: 23px;
  padding: 5px 3px;
  text-align: center;
  text-rendering: optimizeLegibility;
}
h1.elegantshadow {
  color: #202020;
  background-color: #e7e5e4;
  letter-spacing: .15em;
  text-shadow: 1px -1px 0 #767676, -1px 2px 1px #737272, -2px 4px 1px #767474, -3px 6px 1px #787777;
}
h1.deepshadow {
  color: #e0dfdc;
  background-color: #333;
  letter-spacing: .1em;
  text-shadow: 0 -1px 0 #fff, 0 1px 0 #2e2e2e, 0 2px 0 #2c2c2c, 0 3px 0 #2a2a2a, 0 4px 0 #282828, 0 5px 0 #262626, 0 6px 0 #242424, 0 7px 0 #222, 0 8px 0 #202020, 0 9px 0 #1e1e1e, 0 10px 0 #1c1c1c, 0 11px 0 #1a1a1a, 0 12px 0 #181818, 0 13px 0 #161616, 0 14px 0 #141414, 0 15px 0 #121212, 0 22px 30px rgba(0, 0, 0, 0.9);
}
h1.insetshadow {
  color: #202020;
  background-color: #2d2d2d;
  letter-spacing: .1em;
  text-shadow: -1px -1px 1px #111, 2px 2px 1px #363636;
}
h1.retroshadow {
  color: #2c2c2c;
  background-color: #d5d5d5;
  letter-spacing: .05em;
  text-shadow: 4px 4px 0px #d5d5d5, 7px 7px 0px rgba(0, 0, 0, 0.2);
}
body {
        background-image: url('/static/micro_carbon.png');
}
section {
        margin: 7px auto 0;
        width: 75px;
        height: 95px;
        position: relative;
        text-align: center;
}
:active, :focus {
        outline: 0;
}
/** Font-Face **/
@font-face {
  font-family: "FontAwesome";
  src: url("/static/fonts/fontawesome-webfont.eot");
  src: url("/static/fonts/fontawesome-webfont.eot?#iefix") format('eot'),
           url("/static/fonts/fontawesome-webfont.woff") format('woff'),
           url("/static/fonts/fontawesome-webfont.ttf") format('truetype'),
           url("/static/fonts/fontawesome-webfont.svg#FontAwesome") format('svg');
  font-weight: normal;
  font-style: normal;
}
/** Styling the Button **/
a {
        font-family: "FontAwesome";
        text-shadow: 0px 1px 1px rgba(250,250,250,0.1);
        font-size: 32pt;
        display: block;
        position: relative;
        text-decoration: none;
    box-shadow: 0px 3px 0px 0px rgb(34,34,34),
                        0px 7px 10px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -12px 35px 0px rgba(0, 0, 0, .5);
        width: 70px;
        height: 70px;
        border: 0;
        color: rgb(37,37,37);
        border-radius: 35px;
        text-align: center;
        line-height: 79px;
        background-color: rgb(83,87,93);

        transition: color 350ms ease, text-shadow 350ms;
                -o-transition: color 350ms ease, text-shadow 350ms;
                -moz-transition: color 350ms ease, text-shadow 350ms;
                -webkit-transition: color 350ms ease, text-shadow 350ms;
}
a:before {
        content: "";
        width: 80px;
        height: 80px;
        display: block;
        z-index: -2;
        position: absolute;
        background-color: rgb(26,27,29);
        left: -5px;
        top: -2px;
        border-radius: 40px;
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
a:active {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
}
a.on {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
        color: #fff;
        text-shadow: 0px 0px 3px rgb(250,250,250);
}
a:active:before, a.on:before {
        top: -5px;
        background-color: rgb(26,27,29);
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
/* Styling the Indicator light */
a + span {
        display: block;
        width: 8px;
        height: 8px;
        background-color: rgb(226,0,0);
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(226,0,0,0.5);
        border-radius: 4px;
        clear: both;
        position: absolute;
        bottom: 0;
        left: 42%;
        transition: background-color 350ms, box-shadow 700ms;
        -o-transition: background-color 350ms, box-shadow 700ms;
        -moz-transition: background-color 350ms, box-shadow 700ms;
        -webkit-transition: background-color 350ms, box-shadow 700ms;
}
a.on + span {
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(135,187,83,0.5);
        background-color: rgb(135,187,83);
}
b {
        font-family: "FontAwesome";
        text-shadow: 0px 1px 1px rgba(250,250,250,0.1);
        font-size: 32pt;
        display: block;
        position: relative;
        text-decoration: none;
    box-shadow: 0px 3px 0px 0px rgb(34,34,34),
                        0px 7px 10px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -12px 35px 0px rgba(0, 0, 0, .5);
        width: 70px;
        height: 70px;
        border: 0;
        color: rgb(37,37,37);
        border-radius: 35px;
        text-align: center;
        line-height: 79px;
        background-color: rgb(83,87,93);

        transition: color 350ms ease, text-shadow 350ms;
                -o-transition: color 350ms ease, text-shadow 350ms;
                -moz-transition: color 350ms ease, text-shadow 350ms;
                -webkit-transition: color 350ms ease, text-shadow 350ms;
}
b:before {
        content: "";
        width: 80px;
        height: 80px;
        display: block;
        z-index: -2;
        position: absolute;
        background-color: rgb(26,27,29);
        left: -5px;
        top: -2px;
        border-radius: 40px;
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
b:active {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
}
b.on {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
        color: #fff;
        text-shadow: 0px 0px 3px rgb(250,250,250);
}
b:active:before, b.on:before {
        top: -5px;
        background-color: rgb(26,27,29);
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
/* Styling the Indicator light */
b + span {
        display: block;
        width: 8px;
        height: 8px;
        background-color: rgb(226,0,0);
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(226,0,0,0.5);
        border-radius: 4px;
        clear: both;
        position: absolute;
        bottom: 0;
        left: 42%;
        transition: background-color 350ms, box-shadow 700ms;
        -o-transition: background-color 350ms, box-shadow 700ms;
        -moz-transition: background-color 350ms, box-shadow 700ms;
        -webkit-transition: background-color 350ms, box-shadow 700ms;
}
b.on + span {
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(135,187,83,0.5);
        background-color: rgb(135,187,83);
}
c {
        font-family: "FontAwesome";
        text-shadow: 0px 1px 1px rgba(250,250,250,0.1);
        font-size: 32pt;
        display: block;
        position: relative;
        text-decoration: none;
    box-shadow: 0px 3px 0px 0px rgb(34,34,34),
                        0px 7px 10px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -12px 35px 0px rgba(0, 0, 0, .5);
        width: 70px;
        height: 70px;
        border: 0;
        color: rgb(37,37,37);
        border-radius: 35px;
        text-align: center;
        line-height: 79px;
        background-color: rgb(83,87,93);

        transition: color 350ms ease, text-shadow 350ms;
                -o-transition: color 350ms ease, text-shadow 350ms;
                -moz-transition: color 350ms ease, text-shadow 350ms;
                -webkit-transition: color 350ms ease, text-shadow 350ms;
}
c:before {
        content: "";
        width: 80px;
        height: 80px;
        display: block;
        z-index: -2;
        position: absolute;
        background-color: rgb(26,27,29);
        left: -5px;
        top: -2px;
        border-radius: 40px;
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
c:active {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
}
c.on {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
        color: #fff;
        text-shadow: 0px 0px 3px rgb(250,250,250);
}
c:active:before, c.on:before {
        top: -5px;
        background-color: rgb(26,27,29);
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
/* Styling the Indicator light */
c + span {
        display: block;
        width: 8px;
        height: 8px;
        background-color: rgb(226,0,0);
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(226,0,0,0.5);
        border-radius: 4px;
        clear: both;
        position: absolute;
        bottom: 0;
        left: 42%;
        transition: background-color 350ms, box-shadow 700ms;
        -o-transition: background-color 350ms, box-shadow 700ms;
        -moz-transition: background-color 350ms, box-shadow 700ms;
        -webkit-transition: background-color 350ms, box-shadow 700ms;
}
c.on + span {
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(135,187,83,0.5);
        background-color: rgb(135,187,83);
}
d {
        font-family: "FontAwesome";
        text-shadow: 0px 1px 1px rgba(250,250,250,0.1);
        font-size: 32pt;
        display: block;
        position: relative;
        text-decoration: none;
    box-shadow: 0px 3px 0px 0px rgb(34,34,34),
                        0px 7px 10px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -12px 35px 0px rgba(0, 0, 0, .5);
        width: 70px;
        height: 70px;
        border: 0;
        color: rgb(37,37,37);
        border-radius: 35px;
        text-align: center;
        line-height: 79px;
        background-color: rgb(83,87,93);

        transition: color 350ms ease, text-shadow 350ms;
                -o-transition: color 350ms ease, text-shadow 350ms;
                -moz-transition: color 350ms ease, text-shadow 350ms;
                -webkit-transition: color 350ms ease, text-shadow 350ms;
}
d:before {
        content: "";
        width: 80px;
        height: 80px;
        display: block;
        z-index: -2;
        position: absolute;
        background-color: rgb(26,27,29);
        left: -5px;
        top: -2px;
        border-radius: 40px;
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
d:active {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
}
d.on {
    box-shadow: 0px 0px 0px 0px rgb(34,34,34),
                        0px 3px 7px 0px rgb(17,17,17),
                        inset 0px 1px 1px 0px rgba(250, 250, 250, .2),
                        inset 0px -10px 35px 5px rgba(0, 0, 0, .5);
    background-color: rgb(83,87,93);
        top: 3px;
        color: #fff;
        text-shadow: 0px 0px 3px rgb(250,250,250);
}
d:active:before, d.on:before {
        top: -5px;
        background-color: rgb(26,27,29);
        box-shadow: 0px 1px 0px 0px rgba(250,250,250,0.1),
                                inset 0px 1px 2px rgba(0, 0, 0, 0.5);
}
/* Styling the Indicator light */
d + span {
        display: block;
        width: 8px;
        height: 8px;
        background-color: rgb(226,0,0);
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(226,0,0,0.5);
        border-radius: 4px;
        clear: both;
        position: absolute;
        bottom: 0;
        left: 42%;
        transition: background-color 350ms, box-shadow 700ms;
        -o-transition: background-color 350ms, box-shadow 700ms;
        -moz-transition: background-color 350ms, box-shadow 700ms;
        -webkit-transition: background-color 350ms, box-shadow 700ms;
}
d.on + span {
        box-shadow: inset 0px 1px 0px 0px rgba(250,250,250,0.5),
                                0px 0px 3px 2px rgba(135,187,83,0.5);
        background-color: rgb(135,187,83);
}
</style>
<body>
        <div id=stats>
            <h1 class='elegantshadow'>
                <section>
                        <a href="#" id="button1">&#xF011;</a>
                        <span></span>
                </section>
            <h1 class='elegantshadow'>
                <section>
                        <b href="#" id="button2">&#xF011;</b>
                        <span></span>
                </section>
            <h1 class='elegantshadow'>
                <section>
                        <c href="#" id="button3">&#xF011;</c>
                        <span></span>
                </section>
            <h1 class='elegantshadow'>
                <section>
                        <d href="#" id="button4">&#xF011;</d>
                        <span></span>
                </section>
        </div>
</body>
</html>''')

    build_index_html.write(process_index_html + '\n')
    build_index_html.close()
    return render_template('index.html')

def run_web_server():
    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 443
    server.thread_pool = 1000
    server.ssl_module            = 'pyopenssl'
    server.ssl_certificate       = 'server.crt'
    server.ssl_private_key       = 'server.key'
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

t1 = Thread(target = run_web_server)
t1.start()
