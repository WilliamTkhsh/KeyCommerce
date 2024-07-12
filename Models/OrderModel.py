from database import db
from sqlalchemy import DateTime
from datetime import datetime

class Order(db.Model):
    __tablename__ = "KC_Orders" 
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer(), db.ForeignKey('KC_Users.id'))
    keyboard_id = db.Column(db.Integer(), db.ForeignKey('KC_Keyboards.id'))
    total_price = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(DateTime, default=datetime.now())
    date_updated = db.Column(DateTime, default=datetime.now())
    status = db.Column(db.String(100))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()