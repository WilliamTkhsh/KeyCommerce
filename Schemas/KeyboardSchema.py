from marshmallow import fields, Schema
from Schemas import SwitchSchema, KeyCapSchema, BoardSchema

class KeyboardSchema(Schema):
    switch = fields.Nested(SwitchSchema.SwitchSchema)
    keycap = fields.Nested(KeyCapSchema.KeyCapSchema)
    board = fields.Nested(BoardSchema.BoardSchema)