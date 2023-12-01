#!/usr/bin/python3

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
# from uuid import uuid4

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on the items")

@blp.route("/items/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """This endpoint GET a specific item by item_id"""
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating an item is not implemented")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """This endpoint GET ALL new items"""
        return items.values()
        
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """This endpoint CREATE new item"""
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while Inserting the Item.")

        return item
