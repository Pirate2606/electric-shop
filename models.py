import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


###############################
###### SETUP APP ##############
###############################

app = Flask(__name__)
app.config['SECRET_KEY'] = "topsecret"


###############################
###### SETUP database #########
###############################

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###############################
###### SETUP LOGIN ############
###############################

login_manager = LoginManager()
# login_manager.refresh_view = 'login'
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

###############################
###### SETUP Models ###########
###############################


class User(db.Model, UserMixin):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(128), unique = True, index = True)
    password = db.Column(db.String(128))
    profile_image = db.Column(db.String(126))
    item = db.relationship('MyCart', backref = 'user', lazy = 'dynamic')

    def __init__(self, email, username, password, profile_image):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.profile_image = profile_image

    def __repr__(self):
        return f"{self.username}"

    def check_password(self, password):
        return check_password_hash(self.password, password)

class MyCart(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, item_name, user_id):
        self.item_name = item_name
        self.user_id = user_id

    def __repr__(self):
        return f"{self.item_name}"
