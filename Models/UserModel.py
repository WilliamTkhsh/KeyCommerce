from database import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

def generate_uuid():
    return uuid4()

class User(db.Model):
    __tablename__ = "KC_Users"
    id = db.Column(db.Integer, primary_key= True, default=str(generate_uuid))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text())

    def __repr__(self):
        return f"<User {self.email}"
    
    def set_password(self, password):
        self.password = generate_password_hash(self.password, password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()        