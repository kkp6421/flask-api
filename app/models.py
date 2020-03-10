from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class TaskTag(db.Model):
    __tablename__ = "tasks_tags"
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    def __repr__(self):
        return "<TaskTag: {task_id: %r, tag_id: %r}>" % (self.task_id, self.tag_id)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    finish_flag = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow())
    finish_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship(
        'Tag',
        secondary=TaskTag.__tablename__,
        back_populates='tasks',
    )
    def __repr__(self):
        return "<Task: {id: %r, text: %r, finish_flag: %r, start_date: %r, finish_date: %r, user_id: %r tags_count: %r}>" \
               % (self.id, self.text, self.finish_flag, self.start_date, self.finish_flag, self.user_id, len(self.tags))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tasks = db.relationship(
        'Task',
        secondary=TaskTag.__tablename__,
        back_populates='tags',
    )
    def __repr__(self):
        return "<Tag: {id: %r, text: %r, user_id: %r, tasks_count: %r}>" \
               % (self.id, self.text, self.user_id, len(self.tasks))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='user')
    tags = db.relationship('Tag', backref='tag')

    @property
    def password(self):
        raise AttributeError('password is not a readable attributes.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: {id: %r, username: %r, email: %r, password_hash: %r, tasks_count: %r, tags_count: %r}>" \
               % (self.id, self.username, self.email, self.password_hash, len(self.tasks), len(self.tags))
