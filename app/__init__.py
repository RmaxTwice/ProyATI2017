import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/uploads")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')


mongo= PyMongo(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app import views