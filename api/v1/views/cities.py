#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string: state_id>/cities', methods=['GET'],
                strict_slashes=False)
def cities(state_id):
    """get all the cities in a list"""
    idstate = storage.get("State", state_id)
    if idstate is None:
        abort(404)
    list_city = []
    for nameCity in state.cities:
        list_city.append(nameCity.to_dict())
    return jsonify(list_city)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                strict_slashes=False)
def cityid(city_id):
    idcity = storage.get("City", city_id)
    if idcity is None:
        abort(404)
    return jsonify(idcity.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(city_id):
    """delete city"""
    idcity = storage.get("City", city_id)
    if idcity is None:
        abort(404)
    idcity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                strict_slashes=False)
def post(state_id):
    """function or route that create a new city"""
    idstate = storage.get('State', state_id)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    info = request.get_json()
    info['state_id'] = state_id
    newCity = City(**info)
    newCity.save()
    return make_response(jsonify(newCity.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                strict_slashes=False)
def put(city_id):
    """function or route that update a city"""
    idcity = storage.get("City", city_id)
    if idcity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for name, value in request.get_json().items():
        if name not in ['id', 'created_at', 'updated_at']:
            setattr(idcity, name, value)
        idcity.save()
        return jsonify(idcity.to_dict(), 200)
