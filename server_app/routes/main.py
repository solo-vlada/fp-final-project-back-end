from flask import Blueprint, request, jsonify, redirect
from ..database.db import db
from ..models.tables import Clothing
from werkzeug import exceptions

main_routes = Blueprint("main", __name__)

@main_routes.route("/", methods=["GET", "POST"])
def index(): 
    if request.method == "GET":
        all_clothing = Clothing.query.all()
        return jsonify(all_clothing[0].item_name)
    else:
        pass

@main_routes.route("/new-listing", methods=["POST"])
def new_listing(): 
    if request.method == "POST":
        new_item = Clothing(item_name=request.form['item_name'], description=request.form['item_desc'], category=request.form['item_cat'], size=request.form['item_size'], user_id=request.form['item_user_id'], on_offer=False, images=request.form['item_images'])

        db.session.add(new_item)
        db.session.commit()

@main_routes.errorhandler(exceptions.Unauthorized)
def handle_401():
    return 'error: 404 Could not verify', 401

@main_routes.errorhandler(exceptions.NotFound)
def handle_404():
    return 'error: 404 Page not found', 404

@main_routes.errorhandler(exceptions.MethodNotAllowed)
def handle_405():
    return 'error: 405 Method is not allowed', 405

@main_routes.errorhandler(exceptions.InternalServerError)
def handle_500():
    return 'error: 500 Internal server error', 500