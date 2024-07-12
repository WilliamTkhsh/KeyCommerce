from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from database import db
from Models.OrderModel import Order
from Models.KeyboardModel import Keyboard
from Models.UserModel import User
from datetime import datetime
from Schemas.OrderSchema import OrderSchema
from Enums.OrderStatus import OrderStatus

class OrdersService:
    def register_order(order):
        keyboard = Keyboard.query.get(order.get('keyboard_id'))

        if not keyboard:
            return jsonify({"message": f"Keyboard of id {order.get('keyboard_id')} doesnt exist", "data": {}}), 500

        new_order = Order(
            keyboard_id = keyboard.id,
            user_id = get_jwt_identity(),
            total_price = keyboard.price,
        )

        new_order.status = OrderStatus.CREATED.value

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
        claims = get_jwt()
        user_id = get_jwt_identity()
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        if claims.get('is_staff') == True:
            order = Order.query.paginate(
                page = page,
                per_page = per_page
            )
        else:
            order = Order.query.filter_by(user_id=user_id).paginate(
                page = page,
                per_page = per_page
            )            

        result = OrderSchema().dump(order, many=True)
        return jsonify({
            "order": result,
        })        
    
    def update_order(id, order):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": f"User of request not found", "data": {}}), 404
        keyboard = Keyboard.query.get(order.get('keyboard_id'))

        if not keyboard:
            return jsonify({"message": f"Keyboard of id {order.get('keyboard_id')} doesnt exist", "data": {}}), 404
        total_price = keyboard.price

        target_order = Order.query.get(id)

        if target_order.user_id != user.id:
            return jsonify({"message": f"User is not owner of this order", "data": {}}), 404

        if not target_order:
            return jsonify({"message": "Order nao existe na base"}), 404
        
        try:
            target_order.keyboard = keyboard
            target_order.total_price = total_price
            target_order.date_updated = datetime.now()
            db.session.commit()
            result = OrderSchema().dump(target_order)
            return jsonify({"message": "Order alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update Order" + str(e), "data": {}}), 500

    def delete_order(id):
        user_id = get_jwt_identity()        
        order = Order.query.get(id)
        if not order:
            return jsonify({"message": "Order nao existe"}), 404
        
        if order.user_id != user_id:
            return jsonify({"message": f"User is not owner of this order", "data": {}}), 404        
        
        try:
            db.session.delete(order)
            db.session.commit()
            result = OrderSchema().dump(order)
            return jsonify({"message": "Pedido deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete Order" + str(e), "data": {}}), 500
        
    def cancel_order(id):
        user_id = get_jwt_identity()        
        order = Order.query.get(id)
        if not order:
            return jsonify({"message": "Order nao existe"}), 404
        
        if order.user_id != user_id:
            return jsonify({"message": f"User is not owner of this order", "data": {}}), 404
        
        order.status = OrderStatus.CANCELLED.value

        try:
            order.date_updated = datetime.now()
            db.session.commit()
            result = OrderSchema().dump(order)
            return jsonify({"message": "Pedido cancelado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update Order" + str(e), "data": {}}), 500