#!/usr/bin/python3
import jwt
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from os import getenv

import models

from blocklist import BLOCKLIST
from db import db
from db_info import username, host, password, database
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


"""
This is my first API building Project
using Flask
"""

db_url = f"mysql+mysqlclient://{username}:{password}@{host}/{database}"

def create_app(db_url=None):
    """ Docs: To be updated"""
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

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked"
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Verify if Admin"""
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expire_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message":"The token has expired.",
                    "error":"token_expired"
                }
            ),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed",
                    "error": "invalid_token"
                }
            ),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # Create all Tables in Database
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
