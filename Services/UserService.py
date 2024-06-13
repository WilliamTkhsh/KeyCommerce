from Models.UserModel import User
from flask import request, jsonify
from Schemas.UserSchema import UserSchema
from database import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

class UserService:
    def create_user():
        if request.method == 'POST':
            json_data = request.get_json()
            user = UserService.get_user_by_email(email = json_data.get('email'))
            
            if user is not None:
                return jsonify({"error" : "Usuario ja existente"}), 409
            
            new_user = User(
                email = json_data.get('email')
            )

            new_user.set_password(password = json_data.get('password'))

            try:
                new_user.save()
                result = UserSchema().dump(new_user)
                return jsonify({"message": "Usuario criado com sucesso!", "data": result}), 201
            except Exception as e:
                return jsonify({"message": "Nao foi possivel criar usuario: " + str(e), "data": {}}), 500

    def login_user():
        data = request.get_json()
        user = UserService.get_user_by_email(username = data.get('email'))
        
        if user is None:
            return jsonify({"error": "Email ainda nao cadastrado"}), 400
        
        if user and (user.check_password(password = data.get('password'))):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            return jsonify(
                {
                    "message": "Logged In",
                    "tokens": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            ) , 200
        
        return jsonify({"error": "Senha invalida para este email"}), 400
    
    def get_all_users(): 
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        users = User.query.paginate(
            page = page,
            per_page = per_page
        )

        result = UserSchema().dump(users, many=True)
        
        return jsonify({
            "users": result,
        })    
    
    def update_user_details(id):
        data = request.get_json()
        email = data.get('email')

        user = User.query.get(id)

        if not user:
            return jsonify({"message": "Usuario nao existe"})
        
        try:
            user.email = email
            db.session.commit()
            result = UserSchema().dump(user)
            return jsonify({"message": "Usuario alterado com sucesso", "data": result}), 201            
        except Exception as e:
            return jsonify({"message": "Failed to update user" + str(e), "data": {}}), 500

    def update_user_password(id):
        data = request.get_json()
        password = User.set_password(data.get('password'))

        user = User.query.get(id)

        try:
            user.password = password
            db.session.commit()
            result = UserSchema().dump(user)
            return jsonify({"message": "Senha alterada com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to update password"+ str(e), "data": {}}), 500

    def delete_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "Usuario nao existe"}), 404
        
        try:
            db.session.delete(user)
            db.session.commit()
            result = UserSchema().dump(user)
            return jsonify({"message": "Usuario deletado com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to delete User" + str(e), "data": {}}), 500

    def get_user_by_id(id):
        user = User.query.get(id)
        if user:
            result = UserSchema().dump(user)
            return jsonify({"message": "Usuario encontrado", "data": result}), 201
        
        return jsonify({"message": "User doesnt exist in database", "data": {}}), 404

    def get_user_by_email(email):
        return User.get_user_by_email(email = email)