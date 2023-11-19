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
    new_store = request.get_json()
    return {"name": new_store["name"], "items": new_store["items"]}, 201
