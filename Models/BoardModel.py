from database import db 

class Board(db.Model):
    __tablename__ = "KC_Boards"    
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    size_name = db.Column(db.String(50))
    size = db.Column(db.String(10))  
    price = db.Column(db.Numeric(precision=10, scale=2))
    amount = db.Column(db.Integer)   
    image_url = db.Column(db.String(100)) 

    keyboard = db.relationship('Keyboard', backref='board', lazy=True)

    def set_size_name(self):
        match self.size:
            case "100%":
                self.size_name = "Full-Sized"
            case "96%":
                self.size_name = "Compact Full-Sized"
            case "80%":
                self.size_name = "Tenkeyless"
            case "75%":
                self.size_name = "Compact Tenkeyless"
            case "65%":
                self.size_name = "Compact"   
            case "60%":
                self.size_name = "Mini"
            case _:
                self.size_name = ""

    def get_key_amount(self):
        match self.size:
            case "100%":
                return 104
            case "96%":
                return 100
            case "80%":
                return 87
            case "75%":
                return 84
            case "65%":
                return 68   
            case "60%":
                return 61                                                         

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()        