from flask import Blueprint, request, jsonify
from ..database.db import db
from ..models.tables import Clothing
from werkzeug import exceptions

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

# handles retriving of all/personal listings with optional filter by category
@main_routes.route("/", methods=["GET"])
def index(): 
    if request.method == "GET":
        try:
            category_filter = request.args.get('category', default=None, type=str)
            user_listings = request.args.get('user', default=None, type=str)
            all_clothing = None 

            if user_listings is not None:
                if category_filter is not None:
                    all_clothing = Clothing.query.filter_by(user_id = user_listings,  category=category_filter)
                else:
                    all_clothing = Clothing.query.filter_by(user_id = user_listings)
            else:
                if category_filter is not None:
                    print(category_filter)
                    all_clothing = Clothing.query.filter_by(category = category_filter)
                else:
                    print(category_filter)
                    all_clothing = Clothing.query.all()

            return jsonify([*map(clothing_serializer, all_clothing)]), 200
        except:
            return handle_400()

@main_routes.errorhandler(exceptions.BadRequest)
def handle_400():
    return 'error: 400 Bad request', 400

@main_routes.errorhandler(exceptions.NotFound)
def handle_404():
    return 'error: 404 Page not found', 404

@main_routes.errorhandler(exceptions.InternalServerError)
def handle_500():
    return 'error: 500 Internal server error', 500

@main_routes.errorhandler(exceptions.MethodNotAllowed)
def handle_405():
    return 'error: 405 Method is not allowed', 405
