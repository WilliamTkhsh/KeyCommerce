from database import db 

class Switch(db.Model):
    __tablename__ = "KC_Switches"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    unit_price = db.Column(db.Numeric(precision=10, scale=2))
    type = db.Column(db.String(200))
    sound = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    