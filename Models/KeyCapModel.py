from database import db 

class KeyCap(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(precision=10, scale=2))
    amount = db.Column(db.Integer)