#!/usr/bin/python3
"""create a file index.py"""
from flask import jsonify
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

@app_views.route('/status', strict_slaches=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})
