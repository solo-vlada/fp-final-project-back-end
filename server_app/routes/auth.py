from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
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
   data = request.get_json() 
   hashed_password = generate_password_hash(data['password'], method='sha256')
 
   new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})