#!/usr/bin/python3

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from uuid import uuid4

# from db import stores
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on the Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """This endpoint GET a specific store by store_id"""
        try:
            return stores[store_id]
        except KeyError:
            abort(404, Message="Store Not Found")

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
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """This endpoint GET ALL stores"""
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """ This endpoint POST new store with a unique id"""
        for store in stores.values():
            if (
                store_data["name"] == store ["name"]
                ):
                abort(400, message="Store Already Exist")
        store_id = uuid4().hex
        new_store = {**store_data, "id": store_id}
        # new_store = {**request_store, id}
        stores[store_id] = new_store
        return new_store, 201
