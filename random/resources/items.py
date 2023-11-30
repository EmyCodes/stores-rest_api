#!/usr/bin/python3

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from uuid import uuid4

from db import items
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on the items")

@blp.route("/items/<string:item_id>")
class Items(MethodView):
    def get(self, item_id):
        """This endpoint GET a specific item by item_id"""
        # if items["item_id"] not in items:
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
    

    def put(self, item_id):
        item_data = request.get_json()
        if (
            "name" not in item_data or
            "price" not in item_data
        ):
            abort(400, message="Bad Request. Ensure you include 'name' and 'price' in JSON Payload")
        try:
            # items[item_id] = item_data
            items[item_id] |= item_data
            print({"Message": "Item Updated Successfully!"})
            return items[item_id]
        except KeyError:
            abort(404, message="Item Not Found!")



@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        """This endpoint GET ALL new items"""
        return items.values()

    def post(self):
        """This endpoint CREATE new item"""
        item_data = request.get_json()

        #Error handling
        if (
            "name" not in item_data or
            "price" not in item_data or
            "store_id" not in item_data
        ):
            abort(400, message="Bad Request! Ensure 'name', 'price',\
                'store_id' are in the JSON Payload")
            
        # Check if the key exists
        for item in items.values():
            if (
                item_data["name"] == item["name"] and
                item_data["store_id"] == item["store_id"]
            ):

                abort(400, message="Item Already Exist")
        
        item_id = uuid4().hex
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item
        return new_item, 201
