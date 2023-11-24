#!/usr/bin/python3

from flask import Flask, request
from uuid import uuid4
from db import stores, items

"""
This is my first API building Project
using Flask
"""
app = Flask(__name__)


@app.get("/store")
def get_all_stores():
    """This endpoint GET ALL stores"""
    return {"stores": list(stores.values())}


@app.post("/store")
def post_stores():
    """This endpoint POST new store with a unique id"""
    store_data = request.get_json()
    store_id = uuid4().hex
    new_store = {**store_data, "id": store_id}
    # new_store = {**request_store, id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def create_item():
    """This endpoint CREATE new store"""
    item_data = request.get_json()
    # if item_data[store_id] not in stores:
    #     return f"Message: {name} not found", 404
    item_id = uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


@app.get("/item")
def get_all_items():
    """This endpoint GET ALL new items"""
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>")
def get_one_store(store_id):
    """This endpoint GET a specific store by store_id"""
    try:
        return stores[store_id]
    except KeyError:
        return {"Message": "Store Not Found"}, 404


@app.get("/item/<string:item_id>")
def get_one_item(item_id):
    """This endpoint GET a specific item by item_id"""
    # if items["item_id"] not in items:
    try:
        return items[item_id]
    except KeyError:
        return {"Message": "Item Not Found"}, 404
