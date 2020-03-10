from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

moment = Moment()
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

def create_app(config_name):

    app = Flask(__name__, template_folder="../dist")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .tag import tag as tag_blueprint
    app.register_blueprint(tag_blueprint, url_prefix='/api/tags')

    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/api/tasks')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    return app

