from flask import Blueprint, request, jsonify

auth_routes = Blueprint("auth", __name__)

@auth_routes.get("/login")
def login():
    return "This could be a login page."
