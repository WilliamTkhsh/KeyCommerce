from flask import request, jsonify
from database import db
from Models.KeyCapModel import KeyCap
from Schemas.KeyCapSchema import KeyCapSchema
from Services.UserService import UserService

class KeyCapsService:
    def register_keycap(keycap):        
        if not UserService.user_is_admin():
            return jsonify({"message": "User unauthorized to perform this method"}), 401         
        new_keycap = KeyCap(
            name = keycap.get('name'),
            size = keycap.get('size'),
            price = keycap.get('price'),
            amount = keycap.get('amount')
        )

        try:
            new_keycap.save()
            result = KeyCapSchema().dump(new_keycap)
            return jsonify({"message": "KeyCap registrado com sucesso!", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Nao foi possivel registrar keycap: " + str(e), "data": {}}), 500

    def get_by_id(id):
        keycap = KeyCap.query.get(id)
        if keycap:
            result = KeyCapSchema().dump(keycap)
            return jsonify({"message": "KeyCap encontrado", "data": result}), 201
        
        return jsonify({"message": "KeyCap doesnt exist in database", "data": {}}), 404
    
    def get_paginated_keycaps():
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        keycap = KeyCap.query.paginate(
            page = page,
            per_page = per_page
        )

        result = KeyCapSchema().dump(keycap, many=True)
        
        return jsonify({
            "keycap": result,
        })
    
    def update_keycap(id, keycap):
        if not UserService.user_is_admin():
            return jsonify({"message": "User unauthorized to perform this method"}), 401         
        name = keycap.get('name')
        size = keycap.get('size')
        price = keycap.get('price')
        amount = keycap.get('amount')        
        target_keycap = KeyCap.query.get(id)

        if not target_keycap:
            return jsonify({"message": "KeyCap nao existe na base"})
        
        try:
            target_keycap.name = name
            target_keycap.size = size
            target_keycap.price = price
            target_keycap.amount = amount
            db.session.commit()
            result = KeyCapSchema().dump(target_keycap)
            return jsonify({"message": "KeyCap alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update KeyCap" + str(e), "data": {}}), 500

    def delete_keycap(id):
        if not UserService.user_is_admin():
            return jsonify({"message": "User unauthorized to perform this method"}), 401         
        keycap = KeyCap.query.get(id)
        if not keycap:
            return jsonify({"message": "KeyCap nao existe"}), 404
        
        try:
            db.session.delete(keycap)
            db.session.commit()
            result = KeyCapSchema().dump(keycap)
            return jsonify({"message": "KeyCap deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete KeyCap" + str(e), "data": {}}), 500