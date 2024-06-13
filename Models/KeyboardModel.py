from database import db 

class KeyBoard(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    switch = db.Column(db.PickleType)
    board = db.Column(db.PickleType)
    keycap = db.Column(db.PickleType)
    price = db.Column(db.Numeric(precision=10, scale=2))