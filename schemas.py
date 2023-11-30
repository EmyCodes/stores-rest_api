#!/usr/bin/python3

from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    """Docs: To be Updated """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    """Docs: To be Updated """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    """Docs: To be Updated """
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    """Docs: To be Updated """
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainItemSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """Docs: To be Updated """
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)
