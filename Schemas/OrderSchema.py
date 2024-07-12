from marshmallow import fields, Schema

class OrderSchema(Schema):
    id = fields.Integer()
    user_id = fields.String()
    keyboard_id = fields.Integer()
    total_price = fields.Float()
    date_created = fields.DateTime()
    date_updated = fields.DateTime()
    status = fields.String()