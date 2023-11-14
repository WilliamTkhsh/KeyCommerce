from flask import Flask, Response, Request
from flask_sqlalchemy import SQLAlchemy
import json
from database import db

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'my-key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/mysql"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

@app.route('/')
def Index():
    return "Hello from Flask"

if __name__ == "__main__":
    app.run(debug=True)

