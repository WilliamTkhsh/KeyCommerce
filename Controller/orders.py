from flask import Blueprint, request
from flask_cors import cross_origin
from Services.OrdersService import OrdersService
from flask_jwt_extended import jwt_required


order_route = Blueprint("orders", __name__)

# CREATE
@order_route.route('/create', methods=['POST'], endpoint = "create")
@jwt_required()
@cross_origin()
def create():
    json_data = request.get_json()    
    return OrdersService.register_order(order=json_data)

# READ
@order_route.route('', methods=['GET'], endpoint = "get_all_orders")
@jwt_required()
@cross_origin()
def get_paginated():
    return OrdersService.get_paginated_orders()

# UPDATE
@order_route.route('/<id>', methods=['PUT'], endpoint = "update_order")
@jwt_required()
@cross_origin()
def update(id):
    json_data = request.get_json()        
    return OrdersService.update_order(id, order=json_data)

# DELETE
@order_route.route('/<id>', methods=['DELETE'], endpoint = "delete_order")
@jwt_required()
@cross_origin()
def delete(id):
    return OrdersService.delete_order(id)