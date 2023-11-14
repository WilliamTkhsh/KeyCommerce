from database import db 

class Switch(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(precision=10, scale=2))
    type = db.Column(db.String(200))
    sound = db.Column(db.Integer)
    sound_level = db.Column(db.Integer)
    is_available = db.Column(db.Boolean)
    amount = db.Column(db.Integer)