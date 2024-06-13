from flask import Blueprint, jsonify
from flask_cors import cross_origin
from Services.UserService import UserService


user_route = Blueprint("user", __name__)

@user_route.route('/signup', methods=['POST'])
@cross_origin()
def create_user():
    return UserService.create_user()
    
@user_route.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    return UserService.login_user()

@user_route.route('/all', methods= ['GET'])
@cross_origin()
def get_all_users(): 
    return UserService.get_all_users()

@user_route.route('/<id>', methods= ['GET'])
@cross_origin()
def get_user(id): 
    return UserService.get_user_by_id(id)

@user_route.route('/<id>', methods= ['PUT'])
@cross_origin()
def update_user(id): 
    return UserService.update_user_details(id)

@user_route.route('/password/<id>', methods= ['PUT'])
@cross_origin()
def update_user_password(id): 
    return UserService.update_user_password(id)

@user_route.route('/<id>', methods= ['DELETE'])
@cross_origin()
def delete_user(id): 
    return UserService.delete_user(id)

@user_route.route('/hello', methods=['GET'])
@cross_origin()
def hello():
    return jsonify({"message": "hello"})