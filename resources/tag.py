#!/usr/bin/python3

from flask import request
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

# Blueprint for the Tags
blp = Blueprint("Tags", __name__, description="Operations on the tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    """This is a class for the tags endpoints"""
    @jwt_required() # Newly Added
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """
        This endpoint GET all tags in a specific store by store_id
        Args:
            store_id (int): The id of the store
            Returns: The tags in the store with the given id or 404 if not found
        """
        store = StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()
    
    @jwt_required() # Newly Added
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        """
        This endpoint POST a specific tag by store_id
        Args:
            store_id (int): The id of the store
            Returns: The tag with the given id or 500 if SQLAlchmeyError
        """
        # if TagModel.query.filter(
        #     TagModel.store_id == store_id,
        #     TagModel.name == tag_data["name"]
        # ).first():
        #     abort(400,
        #           message="A tag with that name already exists in the store"
        #           )
            
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
            )

        return tag


@blp.route("/item/<int:item_id>/tag/<string:tag_id>")
class LinkTagsToItems(MethodView):
    """This is a class for the tags endpoints"""
    @jwt_required() # Newly Added
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        """
        This endpoint POST a specific tag by store_id
        Args:
            store_id (int): The id of the store
            Returns: The tag with the given id or 500 if SQLAlchmeyError
        """
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        # To be checked:
        # Item store_id should match Tag store_id
        if item.store_id == tag.store_id:
            item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while Inserting the Tag")
        

        return tag
    
    @jwt_required() # Newly Added
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        """
        This endpoint POST a specific tag by store_id
        Args:
            store_id (int): The id of the store
            Returns: The tag with the given id or 500 if SQLAlchmeyError
        """
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.stores_id == tag.stores_id:
            item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error Occurred while removing the Tag")
        

        return {"message": "Item removed form tag", "item": item, "tag": tag}
 

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    """This is a class for the tags endpoints"""
    @jwt_required() # Newly Added
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """
        This endpoint GET a specific tag by tag_id
        Args:
            tag_id (int): The id of the tag
            Returns: The tag with the given id or 404 if not found
        """
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required() # Newly Added
    @blp.response(
        202,
        description="Deletes a Tag if no item is tagged with it.",
        example={"message": "Tag Deleted."}
    )
    @blp.alt_response(404, description="Tag not Found")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted."
    )
    def delete(self, tag_id):
        """
        This endpoint DELETE a specific tag by tag_id
        Args:
            tag_id (int): The id of the tag
            Returns: The tag with the given id or 404 if not found
        """
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(
            400,
            message="Oops! Could not delete trag. Make sure tag is not associated with any items, then Try Again"
        )
