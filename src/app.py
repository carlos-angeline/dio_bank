import os

import click
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


@click.command("init-db")
def init_db_command():
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///dio_bank.sqlite",
    )

    if test_config is None:

        app.config.from_pyfile("config.py", silent=True)
    else:

        app.config.from_mapping(test_config)

    # Register CLI commands
    app.cli.add_command(init_db_command)

    # initialize extentions
    db.init_app(app)

    return app
