#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SCRAPPER TORRENT

"""
import os
import signal
import subprocess

from flask import Flask
from flask import json
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask_bootstrap import Bootstrap
from ModuloLogica.ManagerLogica import ManagerLogica
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.secret_key = "secrett"
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

managerlogica = ManagerLogica()


###### admin ###########
@app.route("/admin", methods=["GET"])
def home_admin():
    if "usuario" in session and "password" in session:
        # comprobar que este correcto
        return redirect(url_for("admin_profile"))

    context = {}
    if "intentos" in session:
        context["intentos"] = session["intentos"]

    return render_template("admin_login.html", context=context)


@app.route("/admin", methods=["POST"])
def recibir_login_admin():
    if request.form["usuario"] == "" or request.form["password"] == "":
        intentos = session["intentos"]
        intentos += 1
        session["intentos"] = intentos

        return redirect(url_for("home_admin"))

    ok = managerlogica.comprobaradmin(request.form["usuario"], request.form["password"])
    if ok == True:
        # pa delante
        session["usuario"] = request.form["usuario"]
        session["password"] = request.form["password"]

        return redirect(url_for("admin_profile"))
    else:
        # 3 intentos y pa casa
        pass

    return redirect(url_for("home_admin"))


@app.route("/admin_profile", methods=["GET"])
def admin_profile():
    ok = comprobarusuariopassword()
    if ok == False:
        return redirect(url_for("home_admin"))

    return render_template("admin_profile.html")


@app.route("/admin_profile/alta_peliculas", methods=["GET"])
def alta_peliculas_get():
    # resultados = managerlogica.set_peliculas()
    if "resultados" in session:
        resultados = session["resultados"]

        return render_template("alta_peliculas.html", resultados=resultados)
    return render_template("alta_peliculas.html")


@app.route("/admin_profile/alta_peliculas", methods=["POST"])
def alta_peliculas_post():
    # l = "<div>hola</div>"
    # return l  # json.jsonify(l)
    # proceso = subprocess.check_output(["python", "scrappyimagen_filmaffinity.py", "Joker"],  # shell=True,
    #                                   encoding="utf-8", universal_newlines=True)
    # imagen = str(proceso).splitlines()[0]
    # pwd = os.path.abspath(os.curdir)
    for i in range(0, 3):
        proceso = subprocess.run(["python", "scrappyimagen_filmaffinity.py", "Joker"], shell=True, encoding="utf-8",
                                  universal_newlines=True)
        imagen = str(proceso).splitlines()[0]
        send()

        return "63345<br>"
    # proceso = subprocess.check_output(["python", "scrappyimagen_filmaffinity.py", "Joker"],  shell=True,
    #                                   encoding="utf-8", universal_newlines=True, preexec_fn=os.setsid)
    # imagen = proceso.stdout.read()

    # os.killpg(os.getpgid(proceso.pid), signal.SIGTERM)

    if "blockedform" in session:
        if session["blockedform"] == True:
            return redirect(url_for("alta_peliculas_get"))

    if "maxpaginas" in request.form:
        session["blockedform"] = True
        try:
            maxpaginas = int(request.form["maxpaginas"])
            resultados = []
            for current_pagina in range(0, maxpaginas):
                l = managerlogica.set_peliculas(current_pagina)
                resultados.append(l)
                return "<div class="">{0}</div>".format(l)

            session["resultados"] = resultados
        except ValueError:
            raise Exception("Valor no posible convertir {0}".format(request.form["maxpaginas"]))

    return redirect(url_for("alta_peliculas_get"))


@app.route("/admin_profile/alta_series", methods=["GET"])
def alta_series():
    pass
    # resultado = managerlogica.set_peliculas()
    #
    # return render_template("alta_peliculas.html")


@app.route("/admin_profile/ver_productos", methods=["GET"])
def ver_productos():
    resultado = managerlogica.set_peliculas()

    return render_template("ver_productos.html")


####### web #########
@app.route("/", methods=["GET"])
def home():
    # fecha = managermongo.getLastFecha()
    # if fecha != None:

    if "datos" in session:
        if len(session["datos"]) > 0:
            datos = session["datos"]
            return render_template("index.html", datos=datos)

    return render_template("index.html", links=None)


@app.route("/", methods=["POST"])
def recibirDatosHome():
    if "peliculas" in request.form:
        datos = managerlogica.getpeliculas()
        session["datos"] = datos

    elif "series" in request.form:
        series = managerlogica.getseries()
        session["datos"] = series

    return redirect(url_for("home"))


def comprobarusuariopassword():
    if "usuario" not in session or "password" not in session:
        return False
    elif "usuario" in session and "password" in session:
        ok = managerlogica.comprobaradmin(session["usuario"], session["password"])
        return ok
    return False


if __name__ == '__main__':
    socketio.run(app)
    # socketio.run(app, host="127.0.0.1", port=5000, debug=True)
    # app.run("127.0.0.1", 5000, debug=True)
