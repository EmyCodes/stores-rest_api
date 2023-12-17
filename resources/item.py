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


 # Blueprint for the items
blp = Blueprint("items", __name__, description="Operations on the items")


@blp.route("/item/<int:item_id>")
class Store(MethodView):
    """This is a class for the item endpoints"""
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """
        This endpoint GET a specific item by item_id
        Args:
            item_id (int): The id of the item
            Returns: The item with the given id or 404 if not found
        """
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    # @jwt_required(fresh=True)
    @jwt_required()
    def delete(self, item_id):
        """
        This endpoint DELETE a specific item by item_id
        Args:
            item_id (int): The id of the item
            Returns: The item with the given id or 401 if not admin
        """
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            # return {"message": "Admin privilege reqiuired."}, 401
            abort(401, message="Admin privilege reqiuired.")

        item = ItemModel.query.get_or_404(item_id)
        # item = ItemModel.query.filter_by(id=item_id).first()
        try:
            db.session.delete(item)
            db.session.commit()
            return {"message": f"Item with item_id '{item_id}' successfully deleted"}
        except IntegrityError:
            abort(
                400,
                message="Item Not Found"
            )      
    
    # @jwt_required(fresh=True)
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """
        This endpoint UPDATE a specific item by item_id
        Args:
            item_id (int): The id of the item
            Returns: The item with the given id or 400 if an error occurred
        """
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
    """This is a class for the item endpoints"""
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """
        This endpoint GET all items
        Returns: All items
        """
        return ItemModel.query.all()

    # @jwt_required(fresh=True)  
    @jwt_required()  
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """
        This endpoint POST a new item
        Args:
            item_data (dict): The data of the item
            Returns: The item with the given id or 500 if an error occurred while inserting the item
        """
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while Inserting the Item.")

        return item
