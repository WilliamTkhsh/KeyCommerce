from database import db 

class Keyboard(db.Model):
    __tablename__ = "KC_Keyboards"  
    id = db.Column(db.Integer, primary_key= True)
    switch_id = db.Column(db.Integer, db.ForeignKey('KC_Switches.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('KC_Boards.id'))
    keycap_id = db.Column(db.Integer, db.ForeignKey('KC_KeyCaps.id'))
    price = db.Column(db.Numeric(precision=10, scale=2))
    order = db.relationship('Order', backref='keyboard', lazy=True)    

    def set_price(self):
        return self.switch.unit_price + self.keycap.price + self.board.price


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()        