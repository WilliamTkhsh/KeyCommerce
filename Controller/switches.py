from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from Services.SwitchService import SwitchService


switch_route = Blueprint("switches", __name__)

# CREATE
@switch_route.route('/create', methods=['POST'])
@cross_origin()
def create():
    json_data = request.get_json()
    return SwitchService.register_switch(switch=json_data)

# READ
@switch_route.route('/', methods=['GET'])
@cross_origin()
def get_paginated():
    return SwitchService.get_paginated_switches()

# UPDATE
@switch_route.route('/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    json_data = request.get_json()    
    return SwitchService.update_switch(id, switch=json_data)

# DELETE
@switch_route.route('/<id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    return SwitchService.delete_switch(id)