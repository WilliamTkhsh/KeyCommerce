from flask import request, jsonify
from database import db
from Models.OrderModel import Order
from Models.KeyboardModel import Keyboard
from Schemas.OrderSchema import OrderSchema

class OrdersService:
    def register_order(order):
        keyboard = Keyboard.query.get(order.get('keyboard_id'))

        if not keyboard:
            return jsonify({"message": f"Keyboard of id {order.get('keyboard_id')} doesnt exist", "data": {}}), 500

        new_order = Order(
            keyboard_id = keyboard.id,
            total_price = order.get('total_price'),
            payment_type = order.get('payment_type'),
            ship_method = order.get('ship_method'),
        )

        try:
            new_order.save()
            result = OrderSchema().dump(new_order)
            return jsonify({"message": "Order registrado com sucesso!", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Nao foi possivel registrar order: " + str(e), "data": {}}), 500

    def get_by_id(id):
        order = Order.query.get(id)
        if order:
            result = OrderSchema().dump(order)
            return jsonify({"message": "Order encontrado", "data": result}), 201
        
        return jsonify({"message": "Order doesnt exist in database", "data": {}}), 404
    
    def get_paginated_orders():
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        order = Order.query.paginate(
            page = page,
            per_page = per_page
        )

        result = OrderSchema().dump(order, many=True)
        
        return jsonify({
            "order": result,
        })
    
    def update_order(id, order):
        name = order.get('name')
        size = order.get('size')
        price = order.get('price')
        amount = order.get('amount')        
        target_order = Order.query.get(id)

        if not target_order:
            return jsonify({"message": "Order nao existe na base"})
        
        try:
            target_order.name = name
            target_order.size = size
            target_order.price = price
            target_order.amount = amount
            db.session.commit()
            result = OrderSchema().dump(target_order)
            return jsonify({"message": "Order alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update Order" + str(e), "data": {}}), 500

    def delete_order(id):
        order = Order.query.get(id)
        if not order:
            return jsonify({"message": "Order nao existe"}), 404
        
        try:
            db.session.delete(order)
            db.session.commit()
            result = OrderSchema().dump(order)
            return jsonify({"message": "Order deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete Order" + str(e), "data": {}}), 500