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
        if not switch:
            return jsonify({"message": f"Unable to create keyboard: Switch of id {keyboard.get('switch_id')} doesnt exist", "data": {}}), 500
        
        keycap = KeyCap.query.get(keyboard.get('keycap_id'))
        if not keycap:
            return jsonify({"message": f"Unable to create keyboard: KeyCap of id {keyboard.get('keycap_id')} doesnt exist", "data": {}}), 500        
        
        board = Board.query.get(keyboard.get('board_id'))
        if not board:
            return jsonify({"message": f"Unable to create keyboard: Board of id {keyboard.get('board_id')} doesnt exist", "data": {}}), 500        

        if switch.amount == 0 or keycap.amount == 0 or board.amount == 0:
            return jsonify({"message": f"Unable to create keyboard: {switch.name} amount is {switch.amount} | {keycap.name} amount is {keycap.amount} | {board.name} amount is {board.amount}", "data": {}}), 500

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
        switch = Switch.query.get(keyboard.get('switch_id'))
        keycap = KeyCap.query.get(keyboard.get('keycap_id'))
        board = Board.query.get(keyboard.get('board_id'))     
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
            return jsonify({"message": "Keyboard deletado com sucesso", "data": "{id}"}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete Keyboard" + str(e), "data": {}}), 500
        
    def set_price(switch, keycap, board):
        return switch.unit_price*board.get_key_amount() + keycap.price + board.price