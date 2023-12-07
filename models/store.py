#!/usr/bin/python3

from db import db

class StoreModel(db.Model):
    """Docs: ---To be Updated Later"""
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    tags = db.relationship("TagModel", back_populates="stpre", lazy="dynamic")
