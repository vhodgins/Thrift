from mainapp import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
from geoalchemy2 import Geometry




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    image_file = db.Column(db.String(24), nullable=False, default='dflt.jpg')
    business = db.Column(db.Boolean(), nullable=False)
    store = db.relationship('Store', backref='Owner', lazy=True)
    following = db.relationship('Follow', backref='Follower', lazy=True)



    def __repr__(self):
        return f"User('{self.username}, {self.business}')"

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60),nullable=False)
    description = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(60), unique=True, nullable=False)
    img = db.Column(db.String(60), nullable=False, default='store.jpg')
    address = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    items = db.relationship('Item', backref='Store', lazy=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)
    tags = db.Column(db.String(1024), nullable=True)



    def __repr__(self):
        return f"Store('{self.name}, {self.address}')"

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store = db.Column(db.Integer)

    def __repr__(self):
        return f"Follow('{self.user}, {self.store}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(60), nullable=True)
    img = db.Column(db.String(60), nullable=False, default='item.jpg')
    store = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    tags = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return f"Item('{self.description}, {self.type}')"
