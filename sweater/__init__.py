from flask import Flask
from flask_font_awesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'SUPERSU'
font_awesome = FontAwesome(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/docresearcher'
db = SQLAlchemy(app)
manager = LoginManager(app)

from sweater import models, routes

with app.app_context():
    db.create_all()

