#!/usr/bin/python3

from db import db
"""
db (object): SQLAlchemy object imported from db.py file
"""


class ItemModel(db.Model):
    """
    Item Model for creating an item object
    Args:
        __tablename__ (str): The name of the table in the database
        id (int): The id of the item
        name (str): The name of the item
        description (str): The description of the item
        price (float): The price of the item
        store_id (int): The id of the store
        store (object): The store object
        tags (list): The list of tags
    """
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship(
        "TagModel", back_populates="items", secondary="items_tags"
    )
