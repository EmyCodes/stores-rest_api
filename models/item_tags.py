#!/usr/bin/python3

from db import db
"""
db (object): SQLAlchemy object imported from db.py file
"""


class ItemTags(db.Model):
    """
    ItemTags Model for creating a many-to-many relationship
    between items and tags
    Args:
        __tablename__ (str): The name of the table in the database
        id (int): The id of the item_tag
        item_id (int): The id of the item
        tag_id (int): The id of the tag
    """
    __tablename__ = "items_tags"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
