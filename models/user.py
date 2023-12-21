#!/usr/bin/python3

from db import db


class UserModel(db.Model):
    """
    User Model for creating a login object
    Args:
        __tablename__ (str): The name of the table in the database
        id (int): The id of the user
        username (str): The username of the user
        password (str): The password of the user
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
