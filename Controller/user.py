from flask import Blueprint, request
from flask_cors import cross_origin
from Services.UserService import UserService
from flask_jwt_extended import jwt_required

user_route = Blueprint("user", __name__)

@user_route.route('/signup', methods=['POST'], endpoint = "signup")
@cross_origin()
def create_user():
    if request.method == 'POST':
        json_data = request.get_json()
        return UserService.create_user(data=json_data)
    
@user_route.route('/login', methods=['POST'], endpoint = "login")
@cross_origin()
def login():
    json_data = request.get_json() 
    return UserService.login(data=json_data)

@user_route.route('/all', methods= ['GET'], endpoint = "all")
@jwt_required()
@cross_origin()
def get_all_users():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int) 
    return UserService.get_all_users(page, per_page)

@user_route.route('/', methods= ['GET'], endpoint = "get_user")
@jwt_required()
@cross_origin()
def get_user(): 
    return UserService.get_user_by_id()

@user_route.route('/', methods= ['PUT'], endpoint = "update_user")
@jwt_required()
@cross_origin()
def update_user():
    data = request.get_json()    
    return UserService.update_user_details(data)

@user_route.route('/password', methods= ['PUT'], endpoint = "update_user_password")
@jwt_required()
@cross_origin()
def update_user_password():
    data = request.get_json()  
    return UserService.update_user_password(data)

@user_route.route('/', methods= ['DELETE'], endpoint = "delete_user")
@jwt_required()
@cross_origin()
def delete_user(): 
    return UserService.delete_user()