#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SCRAPPER TORRENT

"""

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask_bootstrap import Bootstrap
from ModuloLogica.ManagerLogica import ManagerLogica

app = Flask(__name__)

app.secret_key = "secrett"
bootstrap = Bootstrap(app)

# managerweb = ManagerWeb()
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
def alta_peliculas():

    resultado = managerlogica.set_peliculas()

    return render_template("alta_peliculas.html")

@app.route("/admin_profile/alta_series", methods=["GET"])
def alta_series():

    resultado = managerlogica.set_peliculas()

    return render_template("alta_peliculas.html")


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
    app.run("127.0.0.1", 5000, debug=True)
