from flask import Blueprint, request
from flask_cors import cross_origin
from Services.KeyBoardService import KeyBoardService


keyboard_route = Blueprint("keyboard", __name__)

# CREATE
@keyboard_route.route('/create', methods=['POST'])
@cross_origin()
def create():
    json_data = request.get_json()        
    return KeyBoardService.register_keyboard(keyboard=json_data)

# READ
@keyboard_route.route('', methods=['GET'])
@cross_origin()
def get_paginated():
    return KeyBoardService.get_paginated_keyboards()

# UPDATE
@keyboard_route.route('/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    json_data = request.get_json()        
    return KeyBoardService.update_keyboard(id, keyboard=json_data)

# DELETE
@keyboard_route.route('/<id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    return KeyBoardService.delete_keyboard(id)