import click
from flask.cli import with_appcontext

from . import create_app


app = create_app()

@app.cli.command("user")
@click.argument("fullname",  "username", "email")
@click.option('--role',type=click.Choice([])
@click.option('--region',type=click.Choice([])
@with_appcontext
def create_user(fullname, username, email, region, role):
    pass


@app.cli.command("folders")
def create_user():
    pass
