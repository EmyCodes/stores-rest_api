#!/usr/bin/python3

from db import db

class StoreModel(db.Model):
    """Docs: ---To be Updated Later"""
    __tablename__ = "Stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populate="store", lazy="dynamic")
