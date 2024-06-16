from marshmallow import fields, Schema

class SwitchSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    unit_price = fields.Float()
    type = fields.String()
    sound = fields.Integer()
    amount = fields.Integer()