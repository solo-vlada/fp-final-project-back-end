from email.mime import image
from flask import Blueprint, request, redirect, jsonify, render_template
from ..database.db import db
from ..models.tables import Clothing, User
from werkzeug import exceptions
import json

main_routes = Blueprint("main", __name__)

def clothing_serializer(clothing):
    return {
        "id": clothing.id,
        "item_name": clothing.item_name,
        "description": clothing.description,
        "category": clothing.category,
        "size": clothing.size,
        "user_id": clothing.user_id,
        "on_offer": clothing.on_offer,
        "images": clothing.images
    }

@main_routes.route("/", methods=["GET"])
def index(): 
    if request.method == "GET":
        all_clothing = Clothing.query.all()
        return jsonify([*map(clothing_serializer, all_clothing)]), 200

@main_routes.route("/<string:user_id>", methods=["GET"])
def personal_listings(user_id):
    if request.method == "GET":
        users_listings = Clothing.query.filter_by(user_id = user_id)
        return jsonify([*map(clothing_serializer, users_listings)]), 200

@main_routes.errorhandler(exceptions.NotFound)
def handle_404():
    return 'error: 404 Page not found', 404

@main_routes.errorhandler(exceptions.InternalServerError)
def handle_500():
    return 'error: 500 Internal server error', 500

@main_routes.errorhandler(exceptions.MethodNotAllowed)
def handle_405():
    return 'error: 405 Method is not allowed', 405
