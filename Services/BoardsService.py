from flask import request, jsonify
from database import db
from Models.BoardModel import Board
from Schemas.BoardSchema import BoardSchema

class BoardsService:
    def register_board(board):        
        new_board = Board(
            name = board.get('name'),
            size = board.get('size'),
            price = board.get('price'),
            amount = board.get('amount')
        )

        try:
            new_board.save()
            result = BoardSchema().dump(new_board)
            return jsonify({"message": "Board registrado com sucesso!", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Nao foi possivel registrar board: " + str(e), "data": {}}), 500
        
    def get_by_id(id):
        board = Board.query.get(id)
        if board:
            result = BoardSchema().dump(board)
            return jsonify({"message": "Board encontrado", "data": result}), 201
        
        return jsonify({"message": "Board doesnt exist in database", "data": {}}), 404
    
    def get_paginated_boards():
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        board = Board.query.paginate(
            page = page,
            per_page = per_page
        )

        result = BoardSchema().dump(board, many=True)
        
        return jsonify({
            "board": result,
        })
    
    def update_board(id, board):
        name = board.get('name')
        size = board.get('size')
        price = board.get('price')
        amount = board.get('amount')        
        target_board = Board.query.get(id)

        if not target_board:
            return jsonify({"message": "Board nao existe na base"})
        
        try:
            target_board.name = name
            target_board.size = size
            target_board.price = price
            target_board.amount = amount
            db.session.commit()
            result = BoardSchema().dump(target_board)
            return jsonify({"message": "Board alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update Board" + str(e), "data": {}}), 500

    def delete_board(id):
        board = Board.query.get(id)
        if not board:
            return jsonify({"message": "Board nao existe"}), 404
        
        try:
            db.session.delete(board)
            db.session.commit()
            result = BoardSchema().dump(board)
            return jsonify({"message": "Board deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete Board" + str(e), "data": {}}), 500