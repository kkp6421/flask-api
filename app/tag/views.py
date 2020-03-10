from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from . import tag
from .. import db
from ..models import Tag, User

@tag.route("/", methods=['GET'])
@jwt_required
def index():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    tags = current_user.tags
    return jsonify([{
        "id": t.id,
        "text": t.text
    } for t in tags]), 200

@tag.route("/create", methods=['POST'])
@jwt_required
def create():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        text = request.get_json()["text"]
        if not text:
            return jsonify({"msg": "Missing text parameter"}), 400
        new_tag = Tag(text=text)
        current_user.tags.append(new_tag)
        db.session.add(current_user)
        db.session.commit()
        return jsonify({"msg": "Create tag successfully."}), 200

@tag.route("/delete", methods=['POST'])
@jwt_required
def delete():
    if request.get_json():
        tag_id = request.get_json()["tag_id"]
        if not tag_id:
            return jsonify({"msg": "Missing tag_id parameter"}), 400
        t = Tag.query.filter_by(id=tag_id).first()
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "Delete tag successfully."}), 200
