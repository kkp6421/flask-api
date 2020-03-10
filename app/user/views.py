from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import user
from ..models import User, Tag
from .. import db

@user.route("/info", methods=['GET'])
@jwt_required
def show_info():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        "id": current_user.id,
        "usernmae": current_user.username,
        "email": current_user.email
    }), 200

@user.route("/create", methods=['POST'])
def create():
    if not request.get_json():
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    if not username:
        return jsonify({"msg": "Missing username parameter."}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter."}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter."}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "This email has been used."}), 400
    new_user = User(username=username, email=email, password=password)
    all_text = ["家事", "子供", "夫", "妻", "親", "親戚", "仕事", "学校", "習い事", "部活", "友達", "イベント", "その他"]
    for text in all_text:
        tag = Tag(text=text)
        new_user.tags.append(tag)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "create user successfully."}), 200

