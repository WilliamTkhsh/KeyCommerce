from marshmallow import fields, Schema

class KeyCapSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    size = fields.String()
    price = fields.Float()
    amount = fields.Integer()