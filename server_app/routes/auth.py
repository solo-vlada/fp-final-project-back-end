from ast import match_case
from flask import Blueprint, jsonify, make_response, request, current_app as app, redirect
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
from ..database.db import db
from ..models.tables import User, Messages, Clothing, Offers

auth_routes = Blueprint("auth", __name__)

# Creates a decorator for checking valid json web tokens that can be used to limit methods to valid token users
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator    

# Register new user / expects json post handled by frontend
@auth_routes.route('/register', methods=['POST'])
@cross_origin()
def register_user(): 
    try:
        content = request.json
        hashed_password = generate_password_hash(content['password'], method='sha256')

        new_user = User(
            id = f'{uuid.uuid1()}',
            username = content['username'], 
            password = hashed_password, 
            location = content['location'], 
            email = content['email']
        )

        db.session.add(new_user)
        db.session.commit()   
        return jsonify({'message': 'registered successfully'}), 201
    except:
        return jsonify({'message': 'registration unsuccessful'}), 400

# Login to existing account / expects basic auth containing the username and password
@auth_routes.route('/login', methods=['POST']) 
def login_user():

    # Check that login request was sent with basic auth
    auth = request.authorization
    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify basic auth', 401, {'Authentication': 'login required"'})   
    
    user = User.query.filter_by(username=auth.username).first()  
    if check_password_hash(user.password, auth.password):
    # if user.password == auth.password:
        token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256"), {"user_id": user.id, "username": user.username}

        return jsonify({'token': token}), 200
     
    return jsonify('could not verify'), 401

# Create new clothes item on database
@auth_routes.route("/new-listing", methods=["POST"])
@token_required
def new_listing(current_user): 
    if request.method == "POST":
        content = request.json
        new_item = Clothing(item_name=content['item_name'], description=content['item_desc'], category=content['item_cat'], size=content['item_size'], user_id=content['item_user_id'], on_offer=False, images=content['item_images'])

        db.session.add(new_item)
        db.session.commit()
        return jsonify({"added clothing": f'{new_item}'}), 201

# Send messages between users
@auth_routes.route('/msg', methods=['GET', 'POST'])
@token_required
def messenger_handling(current_user):
    if request.method == 'GET':
        try:
            #  retrieve all messages sent by or too user
            all_messages = Messages.query.filter(Messages.sender == current_user.id and Messages.receiver == current_user.id )

            def message_serializer(message):
                sender = User.query.filter(User.id == message.sender).first()
                reciever  =User.query.filter(User.id == message.receiver).first()
                return {
                    "message_id": message.message_id,
                    "message_date" : message.message_date,
                    "message_text": message.message_text,
                    "sender": message.sender,
                    "receiver": message.receiver,
                    "sender_name": sender.username,
                    "receiver_name": reciever.username
                }
            return jsonify({'Messages': [*map(message_serializer, all_messages)]}), 200
        except:
            return jsonify({'Error': 'Cannot retrieve message\'s from non-existent user'}), 404
    else:
        try:
            # expect message in json format with user_id and receiver_id as the sender and recipient
            current_user = request.json
            new_message = Messages(
                message_text=current_user['message_text'],
                sender=current_user['user_id'],
                receiver=current_user['receiver_id']
            )

            db.session.add(new_message)
            db.session.commit()
            return jsonify({'Message sent': new_message.message_text}), 201
        except:
            print(current_user)
            print(request.json)
            return jsonify({'Error': 'Cannot send message to non-existent user'}), 404

# Propose a swap and assign items to register intent
@auth_routes.route('/create-swap', methods=['POST'])
@token_required
def create_swap(current_user):
    if request.method == "POST":
        try:
            content = request.json
            swap_entry = Offers(
                proposer = current_user,
                proposer_item_id = content['proposer_item_id'],
                reciever = content['reciever'],
                reciever_item_id =content['reciever_item_id'],
                offer_status = "pending"
            )
            print(swap_entry)
            db.session.add(swap_entry)

            proposed_item = Clothing.query.get(swap_entry.proposer_item_id)
            proposed_item.on_offer = True
            print(proposed_item)
            db.session.commit()

            return jsonify({"Success": "Swap entry created"}), 201
        except:
            return jsonify({'Error': 'Cannot swap with non-existent user'}), 404

# update a existing swap entry status with accept, reject or pending
@auth_routes.route('/update-swap-status', methods=['PUT'])
@token_required
def update_swap_status(current_user):
    if request.method == "PUT":
        content = request.json
        status = content['status']

        if status == "accepted":
            offer_entry = Offers.query.get(content['offer_id'])
            offer_entry.offer_status = "accepted"

        elif status == "rejected":
            offer_entry = Offers.query.get(content['offer_id'])
            offer_entry.offer_status = "rejected"

            proposed_item = Clothing.query.get(content['proposer_item_id'])
            proposed_item.on_offer = False

        elif status == "pending":
            offer_entry = Offers.query.get(content['offer_id'])
            offer_entry.offer_status = "pending"

            proposed_item = Clothing.query.get(content['proposer_item_id'])
            proposed_item.on_offer = True

    return jsonify(f"msg: offer #{content['offer_id']} has been updated to: {status}"), 204

@auth_routes.route('/offers', methods=['GET'])
@token_required
def get_all_offers(current_user):
    offers = None
    try:
        user_offers = request.args.get('user', default=None, type=str)
        if user_offers is not None:
            offers = Offers.query.filter_by(proposer = user_offers, reciever= user_offers)
        else:
            offers = Offers.query.all()

        results = []
        for offer in offers:  
            offer_data = {}  
            offer_data['id'] = offer.id 
            offer_data['proposer'] = offer.proposer
            offer_data['proposer_item_id'] = offer.proposer_item_id
            offer_data['reciever'] = offer.reciever
            offer_data['reciever_item_id'] = offer.reciever_item_id
            offer_data['offer_status'] = offer.offer_status
            
            results.append(offer_data)  
        return jsonify({'offers': results}), 200
    except:
        return jsonify({'error': 'Bad request'}), 400

# Test route recieve all users in json format
@auth_routes.route('/users', methods=['GET'])
def get_all_users():
        
    users = User.query.all()
    result = []  
    for user in users:  
        user_data = {}  
        user_data['id'] = user.id 
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['location'] = user.location
        user_data['email'] = user.email
        
        result.append(user_data)  
    return jsonify({'users': result})
