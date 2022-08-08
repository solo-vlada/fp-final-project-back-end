from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ

from .database.db import db
from .routes.main import main_routes
from .routes.auth import auth_routes

from .database.db import db
from .routes.main import main_routes
from .routes.auth import auth_routes 

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


CORS(app)
db.app = app
db.init_app(app)
db.create_all()

app.register_blueprint(main_routes)
app.register_blueprint(auth_routes, url_prefix='/auth')

## Main
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port) 
