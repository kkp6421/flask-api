from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from . import task
from .. import db
from ..models import Task, User

def support_datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


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
        "finish_date_utc": x.finish_date
    } for x in all_tasks])


@task.route("/create", methods=['POST'])
@jwt_required
def create():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        text = request.get_json()["text"]
        if not text:
            return jsonify({
                "msg": "missing text parameter",
                "json": request.get_json()
            })
        new_task = Task(text=text)
        current_user.tasks.append(new_task)
        db.session.add(current_user)
        db.session.commit()
        return jsonify("Create task successfully.")


@task.route("/finish", methods=['POST'])
def finish():
    if request.get_json():
        t = Task.query.filter_by(id=request.get_json()["task_id"])
        t.finish_flag = True
        t.finish_date = datetime.utcnow()
        db.session.add(t)
        db.session.commit()
        return jsonify("Finish task successfully.")

@task.route("/delete", methods=['POST'])
def delete():
    if request.get_json():
        t = Task.query.filter_by(id=request.get_json()["task_id"])
        db.session.delete(t)
        db.session.commit()
        return jsonify("Delete task successfully")
