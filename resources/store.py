#!/usr/bin/python3

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from uuid import uuid4

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on the Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """This endpoint GET a specific store by store_id"""
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": f"Store with store_id {store_id} successfully deleted"}
        except IntegrityError:
            abort(
                400,
                message="Store Not Found"
            )      

    def put(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Updating is not Implentmented")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """This endpoint GET ALL stores"""
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        """ This endpoint POST new store with a unique id"""
        new_store = StoreModel(**store_data)

        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while Inserting the Item.")

        return new_store
