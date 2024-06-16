from flask import request, jsonify
from database import db
from Models.SwitchModel import Switch
from Schemas.SwitchSchema import SwitchSchema

class SwitchService:
    def register_switch(switch):        
        new_switch = Switch(
            name = switch.get('name'),
            unit_price = switch.get('unit_price'),
            type = switch.get('type'),
            sound = switch.get('sound'),
            amount = switch.get('amount')
        )

        try:
            new_switch.save()
            result = SwitchSchema().dump(new_switch)
            return jsonify({"message": "Switch registrado com sucesso!", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Nao foi possivel registrar switch: " + str(e), "data": {}}), 500

    def get_paginated_switches():
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        switch = Switch.query.paginate(
            page = page,
            per_page = per_page
        )

        result = SwitchSchema().dump(switch, many=True)
        
        return jsonify({
            "switch": result,
        })
    
    def update_switch(id, switch):
        name = switch.get('name')
        unit_price = switch.get('unit_price')
        type = switch.get('type')
        sound = switch.get('sound')
        amount = switch.get('amount')

        target_switch = Switch.query.get(id)

        if not target_switch:
            return jsonify({"message": "Switch nao existe na base"})
        
        try:
            target_switch.name = name
            target_switch.unit_price = unit_price
            target_switch.type = type
            target_switch.sound = sound
            target_switch.amount = amount
            db.session.commit()
            result = SwitchSchema().dump(target_switch)
            return jsonify({"message": "Switch alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update Switch" + str(e), "data": {}}), 500

    def delete_switch(id):
        switch = Switch.query.get(id)
        if not switch:
            return jsonify({"message": "Switch nao existe"}), 404
        
        try:
            db.session.delete(switch)
            db.session.commit()
            result = SwitchSchema().dump(switch)
            return jsonify({"message": "Switch deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete Switch" + str(e), "data": {}}), 500