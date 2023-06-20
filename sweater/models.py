from sweater import db, manager
from datetime import datetime
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    recovery_code = db.Column(db.String(6))
    register_time = db.Column(db.DateTime, default=datetime.utcnow)


class Recovery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recovery_code = db.Column(db.String(6))
    recovery_code_expiry = db.Column(db.DateTime)  # новое поле
    user = db.relationship('Users', backref=db.backref('recovery', lazy=True))


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_id = db.Column(db.String(32), nullable=False)
    group = db.Column(db.String(32), nullable=False)
    user = db.relationship('Users', backref=db.backref('files', lazy=True))
    request_time = db.Column(db.DateTime, default=datetime.utcnow)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
