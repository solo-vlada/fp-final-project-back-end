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

@main_routes.route("/", methods=["GET", "POST"])
def index(): 
    if request.method == "GET":
        all_clothing = Clothing.query.all()
        print(type(all_clothing))
        return jsonify([*map(clothing_serializer, all_clothing)]), 200
    else:

        item_name = 'item 1'
        description = "cool item t-shirt"
        category = "t-shirt"
        size = "M"
        user_id = "1"
        on_offer = False
        images = "http:google.com"

        new_clothing = Clothing(item_name=item_name, description=description, category=category, size=size, user_id=user_id, on_offer=on_offer, images=images)

        db.session.add(new_clothing)
        db.session.commit()
        return jsonify({"added clothing": new_clothing}), 201
        

@main_routes.route("/new-listing", methods=["POST"])
def new_listing(): 
    if request.method == "POST":
        content = request.json
        new_item = Clothing(item_name=content['item_name'], description=content['item_desc'], category=content['item_cat'], size=content['item_size'], user_id=content['item_user_id'], on_offer=False, images=content['item_images'])

        db.session.add(new_item)
        db.session.commit()
        return jsonify({"added clothing": f'{new_item}'}), 201

@main_routes.errorhandler(exceptions.NotFound)
def handle_404():
    return 'error: 404 Page not found', 404

@main_routes.errorhandler(exceptions.InternalServerError)
def handle_500():
    return 'error: 500 Internal server error', 500

@main_routes.errorhandler(exceptions.MethodNotAllowed)
def handle_405():
    return 'error: 405 Method is not allowed', 405
