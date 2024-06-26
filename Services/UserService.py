from Models.UserModel import User
from flask import jsonify
import datetime
from Schemas.UserSchema import UserSchema
from database import db
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt

class UserService:
    def create_user(data):
        user = UserService.get_user_by_email(email = data.get('email'))    
        if user is not None:
            return jsonify({"error" : "Usuario ja existente"}), 409
        
        new_user = User(
            email = data.get('email')
        )

        new_user.set_password(password = data.get('password'))

        try:
            new_user.save()
            result = UserSchema().dump(new_user)
            return jsonify({"message": "Usuario criado com sucesso!", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Nao foi possivel criar usuario: " + str(e), "data": {}}), 500

    def login(data):
        user = UserService.get_user_by_email(email = data.get('email'))   
        
        if user is None:
            return jsonify({"error": "Email ainda nao cadastrado"}), 400
        
        if user and (user.check_password(password = data.get('password'))):
            access_token = create_access_token(identity=user.id, expires_delta = datetime.timedelta(hours = 2))
            return jsonify(access_token=access_token, expires_in="2 hours")
        
        return jsonify({"error": "Senha invalida para este email"}), 400

    def get_all_users(page, per_page):
        if not UserService.user_is_admin():
            return jsonify({"message": "User unauthorized to perform this method"}), 401 
        
        users = User.query.paginate(
            page = page,
            per_page = per_page
        )

        result = UserSchema().dump(users, many=True)
        
        return jsonify({
            "users": result,
        })    
    
    def update_user_details(data):
        email = data.get('email')
        id = get_jwt_identity()
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

    def update_user_password(data):
        password = User.set_password(data.get('password'))
        id = get_jwt_identity()
        user = User.query.get(id)

        try:
            user.password = password
            db.session.commit()
            result = UserSchema().dump(user)
            return jsonify({"message": "Senha alterada com sucesso", "data": result}), 201
        except Exception as e:
            return jsonify({"message": "Failed to update password"+ str(e), "data": {}}), 500

    def delete_user():
        id = get_jwt_identity()
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

    def get_user_by_id():
        id = get_jwt_identity()        
        user = User.query.get(id)
        if user:
            result = UserSchema().dump(user)
            return jsonify({"message": "Usuario encontrado", "data": result}), 201
        
        return jsonify({"message": "User doesnt exist in database", "data": {}}), 404

    def get_user_by_email(email):
        return User.get_user_by_email(email = email)
    
    def user_is_admin():
        claims = get_jwt()
        return claims.get('is_staff')
                 