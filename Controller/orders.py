from flask import Blueprint, request
from flask_cors import cross_origin
from Services.OrdersService import OrdersService


order_api = Blueprint("orders", __name__)

# CREATE
@order_api.route('/create', methods=['POST'])
@cross_origin()
def create():
    json_data = request.get_json()    
    return OrdersService.register_order(order=json_data)

# READ
@order_api.route('', methods=['GET'])
@cross_origin()
def get_paginated():
    return OrdersService.get_paginated_orders()

# UPDATE
@order_api.route('/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    json_data = request.get_json()        
    return OrdersService.update_order(id, order=json_data)

# DELETE
@order_api.route('/<id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    return OrdersService.delete_order(id)