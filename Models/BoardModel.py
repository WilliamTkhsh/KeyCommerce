from database import db 

class Board(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    size = db.Column(db.Integer)
    price = db.Column(db.Numeric(precision=10, scale=2))