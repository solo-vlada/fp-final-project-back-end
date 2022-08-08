from urllib import response
from flask import Blueprint, jsonify, make_response, request, current_app as app, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import jwt
import datetime
from ..database.db import db
from ..models.tables import User, Messages

auth_routes = Blueprint("auth", __name__)

# Creates a decorator for checking valid json web tokens
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

# ********************* get all users *********************

def user_serialiser(user):
    return {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'location': user.location,
        'email': user.email
    }

@auth_routes.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        all_users = User.query.all()
        return jsonify([*map(user_serialiser, all_users)])
    elif request.method == 'POST':
        new_user = User(
            username=request.json['username'],
            password=generate_password_hash(request.json['password'], method='sha256'),
            location=request.json['location'],
            email=request.json['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'user created successfully'}), 201

@auth_routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
        user = User.query.get(id)
        return jsonify(user_serialiser(user))

# Login to existing account
@auth_routes.route('/login', methods=['POST']) 
def login_user():

    auth = request.authorization  
    if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
    user = User.query.filter_by(username=auth.username).first()  
    if check_password_hash(user.password, auth.password):
       token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
    return make_response('could not verify',  401, {'Authentication': '"login required"'})

# ********************* get all messages *********************

