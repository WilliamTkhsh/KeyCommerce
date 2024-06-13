from marshmallow import fields, Schema

class UserSchema(Schema):
    id = fields.String()
    email = fields.String()
    password = fields.String()


