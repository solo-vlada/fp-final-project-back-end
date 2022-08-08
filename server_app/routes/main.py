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
        return jsonify([*map(clothing_serializer, all_clothing)])
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
        return {'message': 'added clothing'}
        

@main_routes.route("/new-listing", methods=["POST"])
def new_listing(): 
    if request.method == "POST":
        new_item = Clothing(item_name=request.form['item_name'], description=request.form['item_desc'], category=request.form['item_cat'], size=request.form['item_size'], user_id=request.form['item_user_id'], on_offer=False, images=request.form['item_images'])

        db.session.add(new_item)
        db.session.commit()

@main_routes.route("/test", methods=["GET", "POST"])
def test(): 
    if request.method == "GET":
        new_item = Clothing(item_name="cool hat", description="red", category="hat", size="10", user_id=1, on_offer=False, images="imageurl")

        db.session.add(new_item)
        db.session.commit()

@main_routes.errorhandler(exceptions.NotFound)
def handle_404():
    return 'error: 404 Page not found', 404

@main_routes.errorhandler(exceptions.InternalServerError)
def handle_500():
    return 'error: 500 Internal server error', 500

@main_routes.errorhandler(exceptions.MethodNotAllowed)
def handle_405():
    return 'error: 405 Method is not allowed', 405
