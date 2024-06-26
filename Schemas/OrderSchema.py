from marshmallow import fields, Schema

class OrderSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    keyboard_id = fields.Integer()
    total_price = fields.Float()
    payment_type = fields.String()
    ship_method = fields.String()
    date_created = fields.DateTime()
    status = fields.String()