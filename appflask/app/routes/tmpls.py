from flask import Blueprint, render_template

tmpl = Blueprint("tmpl", __name__)


@tmpl.get("/login")
def login():
    return render_template("/login/login.html")


@tmpl.get("/password")
def password():
    return render_template("/login/password.html")


@tmpl.get("/persons")
def persons():
    return render_template("persons.html")
