#!/usr/bin/python3

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from os import getenv

import models
from db import db
from db_info import username, host, password, database

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


"""
This is my first API building Project
using Flask
"""

db_url = f"mysql+mysqlclient://{username}:{password}@{host}/{database}"

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores RESTFul API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] ="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or  getenv("DATABASE_URL", f"sqlite:///{database}")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)                                     

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "106687186741913238732192922019664271153"
    jwt = JWTManager(app)

    # Create all Tables in Database
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
