from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from ...server_app import app
from ..database.db import db
from ..models.tables import User
import uuid
import jwt
import datetime

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=['GET'])
def login():
    return "This could be a login page."

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