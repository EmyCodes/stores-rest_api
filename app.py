#!/usr/bin/python3

from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
			}
		]
	}
]

@app.get("/store")
def get_stores():
    return [{"stores": stores}]

@app.post("/store")
def post_stores():
    request_store = request.get_json()
    new_store = {"name": request_store["name"], "items": request_store["items"]}
    stores.append(new_store)
    return new_store, 201