#!/usr/bin/python3
import jwt
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
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
using Flask, Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy
and Flask-Migrate to create a RESTful API with JWT Authentication and
SQLite Database. I will be using SQLAlchemy to create a database and
Flask-Migrate to migrate the database. I will be using Flask-JWT-Extended to
create a JWT Token for Authentication and Authorization.
I will be using Flask-Smorest to create
a RESTful API with OpenAPI Documentation.
I will be using Flask-RESTful to create a RESTful API.
"""

# db_url = f"mysql+mysqlclient://{username}:{password}@{host}/{database}"


def create_app(db_url=None):
    """
    Create Flask App and register Blueprints and
    Extensions to it and return it as app object
    """
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores RESTFul API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"

    swagger_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist"
    app.config["OPENAPI_SWAGGER_UI_URL"] = swagger_url

    db_uri_config = db_url or getenv("DATABASE_URL", f"sqlite:///{database}")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri_config

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)    # db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "106687186741913238732192922019664271153"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        """
        Check if token is in blocklist or not and
        return error if token is in blocklist.
        """
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """
        Check if token is revoked or not and
        return error if revoked token is used to access any endpoint.
        """
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked"
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        """
        Check if token is fresh or not and
        return error if not fresh token is used to access fresh endpoint.
        """
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """
        Add claims to JWT token based on identity of user (admin or not)
        Args:
            identity: User identity
            Returns: Dictionary of claims
        """
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expire_token_callback(jwt_header, jwt_payload):
        """
        Check if token is expired or not and
        return error if expired token is used to access any endpoint.
        """
        return (
            jsonify(
                {
                    "message": "The token has expired.",
                    "error": "token_expired"
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        Check if token is invalid or not and
        return error if invalid token is used to access any endpoint.
        """
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
        """
        Check if token is missing or not and
        return error if missing token is used to access any endpoint.
        """
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
    # with app.app_context():
    #     db.create_all()

    # Register Blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
