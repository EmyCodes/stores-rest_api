#!/usr/bin/python3

<<<<<<< HEAD
from flask import Flask, request
# from flask_smorest import abort
from uuid import uuid4
from db import stores, items
=======
from flask import Flask
from flask_smorest import Api

from resources.items import blp as ItemBlueprint
from resources.stores import blp as StoreBlueprint

>>>>>>> main

"""
This is my first API building Project
using Flask
"""
app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores RESTFul API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] ="/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)