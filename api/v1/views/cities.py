#!/usr/bin/python3
"""Create a cities.py"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """get all the cities in a list"""
    idstate = storage.get(State, state_id)
    if idstate is None:
        abort(404)
    list_city = []
    for nameCity in idstate.cities:
        list_city.append(nameCity.to_dict())
    return jsonify(list_city)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cityid(city_id):
    idcity = storage.get(City, city_id)
    if idcity is None:
        abort(404)
    return jsonify(idcity.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(city_id):
    """delete city"""
    idCity = storage.get(City, city_id)
    if idCity is not None:
        storage.delete(idCity)
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post(state_id):
    """function or route that create a new city"""
    idState = storage.get(State, state_id)
    if idState is None:
        abort(404)
    the_json = request.get_json()
    if not the_json:
        abort(400, 'Not a JSON')
    if 'name' not in the_json:
        abort(400, 'Missing name')
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put(city_id):
    """function or route that update a city"""
    the_json = request.get_json()
    if not the_json:
        abort(400, 'Not a JSON')
    idCity = storage.get(City, city_id)
    if idCity is not None:
        for attr, value in request.get_json().items():
            setattr(idCity, attr, value)
        storage.save()
        return jsonify(idCity.to_dict()), 200
    abort(404)
