#!/usr/bin/python3
"""create a file index.py"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


"""Create a global dict"""
dcon = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_num():
    """Endpoint that retrieves the number of each objects by type"""
    objtype = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(objtype), 200
