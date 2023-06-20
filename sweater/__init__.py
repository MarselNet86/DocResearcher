from flask import Flask
from flask_font_awesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'SUPERSU'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'schamsutdin88@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'schamsutdin88@gmail.com'
app.config['MAIL_PASSWORD'] = 'qksjknnlcldvzhpx'

font_awesome = FontAwesome(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/docresearcher'
db = SQLAlchemy(app)
manager = LoginManager(app)
mail = Mail(app)

from sweater import models, routes, forms, recovery, files

with app.app_context():
    db.create_all()

