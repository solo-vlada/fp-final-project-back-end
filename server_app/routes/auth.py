from flask import Blueprint, jsonify, make_response, request, current_app as app
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import jwt
import uuid
import datetime
from ..database.db import db
from ..models.tables import User

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

# Regieter new user
@auth_routes.route('/register', methods=['POST'])
def signup_user(): 
   hashed_password = generate_password_hash(request.form['password'], method='sha256')
 
   new_user = User(
    id=str(uuid.uuid4()), 
    username=request.form['username'], 
    password=hashed_password, 
    location=request.form['location'], 
    email=request.form['email']
    )

   db.session.add(new_user)
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})

# Login to existing account
@auth_routes.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
   user = User.query.filter_by(username=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
   return make_response('could not verify',  401, {'Authentication': '"login required"'})

# Test route reciive all users in json format
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