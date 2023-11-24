#!/usr/bin/python3

from flask import Flask, request
from uuid import uuid4
from db import stores, items

app = Flask(__name__)


@app.get("/store")
def get_all_stores():
    return [{"stores": list(stores.values())}]

@app.post("/store")
def post_stores():
    store_data = request.get_json()
    store_id = uuid4().hex        #feeko93eheue493dhde3
    new_store = {**store_data, "id": store_id}
    # new_store = {**request_store, id}
    stores[store_id] = new_store
    return new_store, 201

@app.post("/items")
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return f"Message: {name} not found", 404
    item_id = uuid4().hex        #feeko93eheue493dhde3
    new_item = {**item_data, "id": item_id}
    stores[item_id] = new_item
    return new_item, 201

@app.get("/items")
def get_all_items():
    return list(items.values())    

@app.get("/store/<string:store_id>")
def get_one_store(store_id):
    try:
        return stores["store_id"]
    except KeyError:
        return "Message: Store Not Found", 404

@app.get("/items/<string:item_id")
def get_one_item(item_id):
    # if items["item_id"] not in items:
    try:
        return items["item_id"]
    except KeyError:
        return "Message: Item Not Found", 404