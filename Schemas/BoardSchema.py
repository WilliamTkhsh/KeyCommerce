from marshmallow import fields, Schema

class BoardSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    size = fields.String()
    price = fields.Float()
    amount = fields.Integer()