import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import  db

migrate = Migrate()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite",
        JWT_SECRET_KEY="super-secret",
    )

    if test_config is None:

        app.config.from_pyfile("config.py", silent=True)
    else:

        app.config.from_mapping(test_config)

    
    # initialize extentions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    #register Blueprints
    from src.controllers import auth, user, role
    
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app
