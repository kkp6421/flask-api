from flask import request, jsonify
from . import auth
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ..models import User
from .. import db

@auth.route("/api/auth", methods=['POST'])
def login():
    if not request.get_json():
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    if not email:
        return jsonify({"msg": "missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "missing password parameter"}), 400
    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        return jsonify({"msg": "But email or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token, "flag": 1}), 200


@auth.route("/api/protected")
@jwt_required
def protected():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }), 200

@auth.route("/api/user/create", methods=['POST'])
def create():
    if not request.get_json():
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    if not username:
        return jsonify({"msg": "missing username parameter"}), 400
    if not email:
        return jsonify({"msg": "missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "missing password parameter"}), 400
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "username": new_user.username, "email": new_user.email})
