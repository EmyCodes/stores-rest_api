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
        pass
    
    def put(self, store_id):
        pass

    def delete(self, store_id):
        pass


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        pass

    def post(self):
        pass