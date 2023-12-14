#!/usr/bin/python3

from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    """Docs: To be Updated """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    """Docs: To be Updated """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    """Docs: To be Updated """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    """Docs: To be Updated """
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    """Docs: To be Updated """
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """Docs: To be Updated """
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    """Docs: To be Updated """
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    """Docs: To be Updated """
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
    """Docs: To be updated """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)