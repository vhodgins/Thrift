from mainapp import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import and_
from sqlalchemy.sql import func





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    charactertype = db.Column(db.Boolean(), nullable=False)
    partycode = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.username}, {self.charactertype}, {self.partycode}')"



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    partycode = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ownername = db.Column(db.String(1000))

    def __repr__(self):
        return f"Message('{self.text},{self.owner}')"


''''
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60),nullable=False)
    description = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(60), unique=True, nullable=False)
    img = db.Column(db.String(60), nullable=False, default='store.jpg')
    address = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    # derived from address

    items = db.relationship('Item', backref='Store', lazy=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)
    tags = db.Column(db.String(1024), nullable=True)

    postLimit = db.Column(db.Integer, nullable=False, default=10)
    # Premium accounts have no post limit and no post expiration

    views = db.Column(db.Integer, nullable=False, default=0)
    # on store load raise count

    lastWeekViews = db.Column(db.Integer, nullable=True)
    # views from last week

    clickthroughs = db.Column(db.Integer, nullable=False, default=0)
    # sum of click throughs from item navigations

    lastWeekClickthroughs = db.Column(db.Integer, nullable=True)
    # click throughs from last week
    numposts = db.Column(db.Integer, nullable=False, default=0)
    # for getting new posts


    def __repr__(self):
        return f"Store('{self.name}, {self.address}')"



class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store = db.Column(db.Integer)
    storeName = db.Column(db.String)
    last_seen = db.Column(db.Integer)

    def __repr__(self):
        return f"Follow('{self.user}, {self.store}')"




class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60), nullable=False)

    type = db.Column(db.String(60), nullable=True)
    # not used

    img = db.Column(db.String(60), nullable=False, default='item.jpg')
    img_width = db.Column(db.Integer, nullable=False)
    img_height = db.Column(db.Integer, nullable=False)

    store = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    tags = db.Column(db.String(60), nullable=True)
    metatags = db.Column(db.String(1024), nullable=True)

    time_left = db.Column(db.Integer, nullable=False, default=7)
    # If items set to disappear weekly

    location = db.Column(db.String(120), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    # same as parent store location

    views = db.Column(db.Integer, nullable=False, default=0)
    # on item view
    clickthroughs = db.Column(db.Integer, nullable=False, default=0)
    # on click to navigate


    @hybrid_method
    def lat_dist(self, lat, n):
        return (abs(self.lat-lat)<n)

    @lat_dist.expression
    def lat_dist(cls, lat, n):
        return (func.abs(cls.lat-lat)<n)

    @hybrid_method
    def lng_dist(self, lng, n):
        return (abs(self.lng - lng)<n)

    @lng_dist.expression
    def lng_dist(cls, lng, n):
        return func.abs(cls.lng - lng)<n



    def __repr__(self):
        return f"Item('{self.description}, {self.type}, {self.time_left}')"
'''