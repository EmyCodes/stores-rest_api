#!/usr/bin/python3

from flask import request
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from uuid import uuid4

from db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema


# Blueprint for the Stores
blp = Blueprint("stores", __name__, description="Operations on the Stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    """This is a class for the store endpoints"""
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """
        This endpoint GET a specific store by store_id
        Args:
            store_id (int): The id of the store
            Returns: The store with the given id or 404 if not found
        """
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        """
        This endpoint DELETE a specific store by store_id
        Args:
            store_id (int): The id of the store
            Returns: The store with the given id or 404 if not found
        """
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": f"Store with store_id "
                    "'{store_id}' successfully deleted"}
        except IntegrityError:
            abort(
                400,
                message="Store Not Found"
            )      

    @jwt_required() # Newly Added
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        """
        This endpoint UPDATE a specific store by store_id
        Args:
            store_id (int): The id of the store
            Returns: The store with the given id or 404 if not found
        """
        store = StoreModel.query.get_or_404(store_id)
        if store:
            store.name = store_data["name"]
        else:
            item = StoreModel(id=store_id, **store)

        try:
            db.session.add(store)
            db.session.commit()
        except Exception:
            abort(
                400,
                message="An Error Occurred"
            )

        return store
        # raise NotImplementedError("Updating is not Implentmented")


@blp.route("/store")
class StoreList(MethodView):
    """This is a class for the store endpoints"""
    @jwt_required() # Newly Added
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """
        This endpoint GET all stores
        Returns: All stores
        """
        return StoreModel.query.all()
    
    @jwt_required() # Newly Added
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        """
        This endpoint POST new store with a unique id
        Args:
            store_data (dict): The data of the store
            Returns: The store with the given id or 400 if integrity error or 500 if SQLAlchemyError"""
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while Inserting the Item.")

        return store
