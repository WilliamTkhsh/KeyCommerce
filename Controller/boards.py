from flask import Blueprint, request
from flask_cors import cross_origin
from Services.BoardsService import BoardsService


board_route = Blueprint("boards", __name__)

# CREATE
@board_route.route('/create', methods=['POST'])
@cross_origin()
def create():
    json_data = request.get_json()        
    return BoardsService.register_board(board=json_data)

# READ
@board_route.route('', methods=['GET'])
@cross_origin()
def get_paginated():
    return BoardsService.get_paginated_boards()

# UPDATE
@board_route.route('/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    json_data = request.get_json()        
    return BoardsService.update_board(id, board=json_data)

# DELETE
@board_route.route('/<id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    return BoardsService.delete_board(id)