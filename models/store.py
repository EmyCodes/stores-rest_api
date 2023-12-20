#!/usr/bin/python3

from db import db
"""
db (object): SQLAlchemy object imported from db.py file
"""


class StoreModel(db.Model):
    """
    Store Model for creating a store object
    Args:
        __tablename__ (str): The name of the table in the database
        id (int): The id of the store
        name (str): The name of the store
        items (list): The list of items
        tags (list): The list of tags
    """
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic"
    )
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
