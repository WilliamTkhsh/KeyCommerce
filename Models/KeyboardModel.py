from database import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    switch = db.Column(db.PickleType)
    board = db.Column(db.PickleType)
    keycap = db.Column(db.PickleType)