from database import db 

class KeyCap(db.Model):
    __tablename__ = "KC_KeyCaps" 
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    size = db.Column(db.String(10))
    price = db.Column(db.Numeric(precision=10, scale=2))
    amount = db.Column(db.Integer)
    image_url = db.Column(db.String(100)) 
    keyboard = db.relationship('Keyboard', backref='keycap', lazy=True)    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()        