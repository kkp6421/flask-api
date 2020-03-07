from . import main
from flask import render_template, jsonify
from ..models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def index(path):
    return render_template('index.html')

@main.route('/api/profile')
@jwt_required
def show_profile():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        "id": current_user.id,
        "usernmae": current_user.username,
        "email": current_user.email
    })
