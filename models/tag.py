#!/usr/bin/python3

from db import db
"""
db (object): SQLAlchemy object imported from db.py file
"""


class TagModel(db.Model):
    """
    Tag Model for creating a tag object
    Args:
        __tablename__ (str): The name of the table in the database
        id (int): The id of the tag
        name (str): The name of the tag
        store_id (int): The id of the store
        store (object): The store object
        items (list): The list of items
    """
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey("stores.id"), nullable=False)
    
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
