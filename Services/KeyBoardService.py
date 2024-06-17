from flask import request, jsonify
from database import db
from Models.KeyboardModel import Keyboard
from Models.SwitchModel import Switch
from Models.KeyCapModel import KeyCap
from Models.BoardModel import Board
from Schemas.KeyboardSchema import KeyboardSchema

class KeyBoardService:
    def register_keyboard(keyboard):
        switch = Switch.query.get(keyboard.get('switch_id'))
        keycap = KeyCap.query.get(keyboard.get('keycap_id'))
        board = Board.query.get(keyboard.get('board_id'))
            
        new_keyboard = Keyboard(
            switch_id=switch.id,
            keycap_id=keycap.id,
            board_id=board.id
        )

        new_keyboard.price = KeyBoardService.set_price(switch, keycap, board)
        
        try:
            new_keyboard.save()
            result = KeyboardSchema().dump(new_keyboard)
            return jsonify({"message": "Keyboard registrado com sucesso!", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Nao foi possivel registrar keyboard: " + str(e), "data": {}}), 500

    def get_paginated_keyboards():
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        keyboard = Keyboard.query.paginate(
            page = page,
            per_page = per_page
        )

        result = KeyboardSchema().dump(keyboard, many=True)
        
        return jsonify({
            "keyboard": result,
        })
    
    def update_keyboard(id, keyboard):
        switch = Switch.query.get(id=keyboard.get('switch_id'))
        keycap = KeyCap.query.get(id=keyboard.get('keycap_id'))
        board = Board.query.get(id=keyboard.get('board_id'))     
        target_keyboard = Keyboard.query.get(id)

        if not target_keyboard:
            return jsonify({"message": "Keyboard nao existe na base"})
        
        try:
            target_keyboard.switch = switch
            target_keyboard.keycap = keycap
            target_keyboard.board = board
            db.session.commit()
            result = KeyboardSchema().dump(target_keyboard)
            return jsonify({"message": "Keyboard alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update Keyboard" + str(e), "data": {}}), 500

    def delete_keyboard(id):
        keyboard = Keyboard.query.get(id)
        if not keyboard:
            return jsonify({"message": "Keyboard nao existe"}), 404
        
        try:
            db.session.delete(keyboard)
            db.session.commit()
            result = KeyboardSchema().dump(keyboard)
            return jsonify({"message": "Keyboard deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete Keyboard" + str(e), "data": {}}), 500
        
    def set_price(switch, keycap, board):
        return switch.unit_price + keycap.price + board.price