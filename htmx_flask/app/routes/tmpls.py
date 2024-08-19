from flask import Blueprint, render_template

tmpl = Blueprint("tmpl", __name__)


@tmpl.get("/persons")
def persons():
    return render_template("persons.html")
