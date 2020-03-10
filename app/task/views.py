from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from . import task
from .. import db
from ..models import Task, User, Tag


@task.route("/", methods=['GET'])
@jwt_required
def index():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    all_tasks = current_user.tasks
    return jsonify([{
        "id": x.id,
        "text": x.text,
        "finish_flag": x.finish_flag,
        "start_date_utc": x.start_date,
        "finish_date_utc": x.finish_date,
        "tags": [{"tag_id": tag.id, "tag_text": tag.text} for tag in x.tags]
    } for x in all_tasks]), 200


@task.route("/create", methods=['POST'])
@jwt_required
def create():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        text = request.get_json()["text"]
        selected_tags_id = request.get_json()["selected_tags_id"]
        if not text:
            return jsonify({"msg": "Missing text parameter"}), 400
        if not selected_tags_id:
            return jsonify({"msg": "Missing selected_tags_id parameter"}), 400
        new_task = Task(text=text)
        for tag_id in selected_tags_id:
            tag = Tag.query.filter_by(id=int(tag_id)).first()
            new_task.tags.append(tag)
        current_user.tasks.append(new_task)
        db.session.add(current_user)
        db.session.commit()
        return jsonify({"msg": "Create task successfully."}), 200


@task.route("/finish", methods=['POST'])
@jwt_required
def finish():
    if request.get_json():
        task_id = request.get_json()["task_id"]
        if not task_id:
            return jsonify({"msg": "Missing task_id parameter."}), 400
        t = Task.query.filter_by(id=request.get_json()["task_id"])
        t.finish_flag = True
        t.finish_date = datetime.utcnow()
        db.session.add(t)
        db.session.commit()
        return jsonify({"msg": "Finish task successfully."}), 200

@task.route("/delete", methods=['POST'])
@jwt_required
def delete():
    if request.get_json():
        task_id = request.get_json()["task_id"]
        if not task_id:
            return jsonify({"msg": "Missing task_id parameter"}), 400
        t = Task.query.filter_by(id=request.get_json()["task_id"])
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "Delete task successfully."}), 200
