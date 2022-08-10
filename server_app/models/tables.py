from email.policy import default
from ..database.db import db
import datetime
from flask_login import UserMixin

class Clothing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    on_offer = db.Column(db.Boolean, default=False, nullable=False)
    images = db.Column(db.String(500), nullable=True)

    def __init__(self, item_name, description, category, size, user_id, on_offer, images):
        self.item_name = item_name
        self.description = description
        self.category = category
        self.size = size
        self.user_id = user_id
        self.on_offer = on_offer
        self.images = images

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)

    def __init__(self, id, username, password, email, location):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.location = location

class Offers(db.Model):
    offer_id = db.Column(db.Integer, primary_key=True)
    proposer = db.Column(db.ForeignKey('user.id'))
    proposer_item_id = db.Column(db.Integer, db.ForeignKey('clothing.id'))
    reciever = db.Column(db.ForeignKey('user.id'))
    reciever_item_id = db.Column(db.Integer, db.ForeignKey('clothing.id'))
    offer_status = db.Column(db.String(80), nullable=False)
    offer_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow()) #proposed extra columns for offer table

    def __init__(self, proposer, proposer_item_id, reciever, reciever_item_id, offer_status):
        self.proposer = proposer,
        self.proposer_item_id = proposer_item_id,
        self.reciever = reciever,
        self.reciever_item_id = reciever_item_id,
        self.offer_status = offer_status,    

class Messages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.ForeignKey('user.id'))
    receiver = db.Column(db.ForeignKey('user.id'))
    message_text = db.Column(db.String(80), nullable=False)
    message_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __init__(self, message_text, sender, receiver):
        self.message_text = message_text
        self.sender = sender
        self.receiver = receiver
