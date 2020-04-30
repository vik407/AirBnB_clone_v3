#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                strict_slashes=False)
def places(city_id):
    """get all cities in a list"""
    list_cities = storage.get(City, city_id)
    if list_cities is None:
        abort(404)
    list_places = []
    for name in list_cities.places:
        list_places.append(name.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                strict_slashes=False)
def placeid(place_id):
    idplace = storage.get(Place, place_id)
    if idplace is None:
        abort(404)
    return jsonify(idplace.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(place_id):
    """delete place"""
    idplace = storage.get(Place, place_id)
    if idplace is None:
        abort(404)
    idplace.delete()
    return (jsonify({})), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                strict_slashes=False)
def post(city_id):
    """function or route that create a new place"""
    idCity = storage.get(City, city_id)
    if idCity is None:
        abort(404)
    the_json = request.get_json()
    if not the_json:
        abort(400, 'Not a JSON')
    if 'user_id' not in the_json:
        abort(400, 'Missing user_id')
    userId = request.get_json()["user_id"]
    idUser = storage.get(User, user_id)
    if idUser is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    newPlace = Place(**request.get_json())
    newPlace.city_id = city_id
    newPlace.user_id = idUser.id
    storage.new(newPlace)
    storage.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                strict_slashes=False)
def put(place_id):
    """function or route that update an amenity"""
    idplace = storage.get(Place, place_id)
    if idplace is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for name, value in request.get_json().items():
        if name not in ['id', 'user_id','city_id', 'created_at',
                        'updated_at']:
            setattr(place, name, value)
        idplace.save()
        return jsonify(idplace.to_dict()), 200
