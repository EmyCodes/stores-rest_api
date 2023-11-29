#!/usr/bin/python3

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from uuid import uuid4

from db import stores


blp = Blueprint("stores", __name__, description="Operations on the Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        """This endpoint GET a specific store by store_id"""
        try:
            return stores[store_id]
        except KeyError:
            abort (404, Message="Store Not Found")

    def delete(self, store_id):
        store_data = request.get_json()
        try:
            del stores[store_id]
            return {"Message": "Store successfully Deleted"}
        except KeyError:
            abort(404, message="Store Not Found!")
    
    def put(self, store_id):
        store_data = request.get_json()
        try:
            stores[store_id] |= store_data
            return dict(stores[store_id])
        except KeyError:
            abort(404, message="Store Not Found!")



@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        """This endpoint GET ALL stores"""
        return {"stores": list(stores.values())}
        
    def post(self):
        """ This endpoint POST new store with a unique id"""
        store_data = request.get_json()
        #Error handling
        if (
            "name" not in store_data
        ):
            abort(400, message="Bad Request! Ensure 'name', 'price',\
                'store_id' are in the JSON Payload")
            
        # Check if the key exists
        for store in stores.values():
            if (
                store_data["name"] == store ["name"] or
                store_data["store_id"] == store[store_id]
            ):
                abort(400, message="Store Already Exist")
        '''
        if store_data["store_id"] not in stores:
        # if store_data["store_id"] != stores[store_id]:    
            abort(400, message="Store Not Found")
        # Else: Update database with the Processed Logic'''
        store_id = uuid4().hex
        new_store = {**store_data, "id": store_id}
        # new_store = {**request_store, id}
        stores[store_id] = new_store
        return new_store, 201
