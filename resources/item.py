#!/usr/bin/python3

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
# from uuid import uuid4

# from db import items
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on the items")

@blp.route("/items/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """This endpoint GET a specific item by item_id"""
        try:
            return items[item_id]
        except KeyError:
            abort(404, Message="Item Not Found")

    def delete(self, item_id):
        item_data = request.get_json()
        if (
            "name" not in item_data and
            "price" not in item_data
        ):
            abort(400, message="Bad Request. Ensure you include 'name' and 'price' in JSON Payload")
        try:
            del items[item_id]
            return {"Message": "Item deleted!"}
        except:
            abort(404, message="Item Not Found")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            # items[item_id] = item_data
            items[item_id] |= item_data
            print({"Message": "Item Updated Successfully!"})
            return items[item_id]
        except KeyError:
            abort(404, message="Item Not Found!")



@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """This endpoint GET ALL new items"""
        return items.values()
        
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        """This endpoint CREATE new item"""
        new_item = ItemModel(**item_data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while Inserting the Item.")

        return new_item
