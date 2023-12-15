#!/usr/bin/python3

# from flask import request
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from uuid import uuid4

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on the items")

@blp.route("/item/<int:item_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """This endpoint GET a specific store by store_id"""
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required(fresh=True) 
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege reqiuired.")

        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
            return {"message": f"Item with item_id '{item_id}' successfully deleted"}
        except IntegrityError:
            abort(
                400,
                message="Item Not Found"
            )      
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item)

        try:
            db.session.add(item)
            db.session.commit()
        except Exception:
            abort(
                400,
                message="An Error Occurred"
            )

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """This endpoint GET ALL new items"""
        return ItemModel.query.all()

    @jwt_required(fresh=True)    
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
