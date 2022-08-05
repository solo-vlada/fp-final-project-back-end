from crypt import methods
from flask import Blueprint, request, jsonify
from ..database.db import db
from ..models.tables import Clothing, User

main_routes = Blueprint("main", __name__)

@main_routes.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        all_clothing = Clothing.query.all()
        return jsonify(all_clothing)
    else:
        pass

