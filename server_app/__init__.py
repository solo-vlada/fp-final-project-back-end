from dotenv import load_dotenv
from os import environ
<<<<<<< Updated upstream
from flask import Flask, render_template, request
from flask_cors import CORS

from .database.db import db
from .routes.main import main_routes
=======
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
import jwt

from .database.db import db
from .routes.main import main_routes
from .routes.auth import auth_routes
from .models.tables import User
>>>>>>> Stashed changes

#load environment variables
load_dotenv()

database_uri = environ.get('DATABASE_URL')

if 'postgres:' in database_uri:
    database_uri = database_uri.replace("postgres:", "postgresql:")

#create app
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
)
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'


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
>>>>>>> Stashed changes

CORS(app)
db.app = app
db.init_app(app)
db.create_all()

app.register_blueprint(main_routes)
# app.register_blueprint(auth_routes, url_prefix='/auth')

## Main

if __name__ == "__main__":
    app.run(debug=True)
