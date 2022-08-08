from email.policy import default
from ..database.db import db

class Clothing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    on_offer = db.Column(db.Boolean, default=False, nullable=False)
    images = db.Column(db.String(80), nullable=True)

    def __init__(self, item_name, description, category, size, user_id, on_offer, images):
        self.item_name = item_name
        self.description = description
        self.category = category
        self.size = size
        self.user_id = user_id
        self.on_offer = on_offer
        self.images = images

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password, email, location):
        self.username = username
        self.password = password
        self.email = email
        self.location = location

class Offers(db.Model):
    offer_id = db.Column(db.Integer, primary_key=True)
    proposer = db.Column(db.ForeignKey('user.id'))
    reciever = db.Column(db.ForeignKey('user.id'))
    offer_status = db.Column(db.Boolean, nullable=False)
    offer_date = db.Column(db.DateTime, nullable=False) #proposed extra columns for offer table
    proposer_item_id = db.Column(db.Integer, db.ForeignKey('clothing.id'))
    reciever_item_id = db.Column(db.Integer, db.ForeignKey('clothing.id'))


    def __init__(self, item_name, description, category, size, user_id, on_offer, images):
        self.item_name = item_name
        self.description = description
        self.category = category
        self.size = size
        self.user_id = user_id
        self.on_offer = on_offer
        self.images = images
