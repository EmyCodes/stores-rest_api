#!/usr/bin/python3

from marshmallow import Schema, fields

"""Define the schemas for the models
    PlainItemSchema: Plain Item Schema
    PlainStoreSchema: Plain Store Schema
    PlainTagSchema: Plain Tag Schema
    ItemUpdateSchema: Item Update Schema
    ItemSchema: Item Schema inherit from PlainItemSchema
    StoreSchema: Store Schema inherit from PlainStoreSchema
    TagSchema: Tag Schema inherit from PlainTagSchema
    TagAndItemSchema: Tag and Item Schema
    UserSchema: User Schema"""


class PlainItemSchema(Schema):
    """
    Plain Item Schema
    Attributes:
        id: Item id
        name: Item name
        price: Item price
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    """
    Plain Store Schema
    Attributes:
        id: Store id
        name: Store name
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    """
    Plain Tag Schema
    Attributes:
        id: Tag id
        name: Tag name
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    """
    Item Update Schema
    Attributes:
        name: Item name
        price: Item price
    """
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    """
    Item Schema inherit from PlainItemSchema
    Attributes:
        store_id: Store id
        store: Store object
    """
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """
    Store Schema inherit from PlainStoreSchema
    Attributes:
        items: List of items
        tags: List of tags
    """
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreUpdateSchema(Schema):
    """
    Store Update Schema
    Attributes:
        name: Store name
    """
    name = fields.Str()


class TagSchema(PlainTagSchema):
    """
    Tag Schema inherit from PlainTagSchema
    Attributes:
        store_id: Store id
        store: Store object
        items: List of items
    """
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    """
    Tag and Item Schema
    Attributes:
        message: Message
        item: Item object
        tag: Tag object
    """
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

# class PlainUserSchema(Schema):
#     """Docs: To be updated """
#     id = fields.Int(dump_only=True)
#     username = fields.Str(required=True)
#     password = fields.Str(required=True, load_only=True)


# class UserSchema(PlainUserSchema):
#     id = fields.Int(load_only=True)
#     users = fields.List(fields.Nested(PlainUserSchema), dump_only=True)

class UserSchema(Schema):
    """User Schema
    Attributes:
        id: User id
        username: User username
        password: User password
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
