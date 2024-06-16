from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from Services.KeyCapsService import KeyCapsService


keycaps_route = Blueprint("keycaps", __name__)

# CREATE
@keycaps_route.route('/create', methods=['POST'])
@cross_origin()
def create():
    json_data = request.get_json()    
    return KeyCapsService.register_keycap(keycap=json_data)

# READ
@keycaps_route.route('', methods=['GET'])
@cross_origin()
def get_paginated():
    return KeyCapsService.get_paginated_keycaps()

# UPDATE
@keycaps_route.route('/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    json_data = request.get_json()        
    return KeyCapsService.update_keycap(id, keycap=json_data)

# DELETE
@keycaps_route.route('/<id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    return KeyCapsService.delete_keycap(id)