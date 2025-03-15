# flask_version/routes.py
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User

def register_routes(app):
    jwt = JWTManager(app)

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        if not data or not all(k in data for k in ("username", "email", "password")):
            return jsonify({"message": "Données manquantes"}), 400
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"message": "Utilisateur existe déjà"}), 400
        user = User(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.check_password(data["password"]):
            return jsonify({"message": "Identifiants invalides"}), 401
        token = create_access_token(identity=user.username)
        return jsonify({"access_token": token})

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def get_profile():
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        return jsonify({"id": user.id, "username": user.username, "email": user.email})

    @app.route("/profile", methods=["PUT"])
    @jwt_required()
    def update_profile():
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        data = request.get_json()
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.set_password(data["password"])
        db.session.commit()
        return jsonify({"message": "Profil mis à jour"})

    @app.route("/profile", methods=["DELETE"])
    @jwt_required()
    def delete_profile():
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Compte supprimé"})