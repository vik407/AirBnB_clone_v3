#!/usr/bin/python3
"""create a file users.py"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/cities/<c_id>/places', strict_slashes=False,
                 methods=['GET'])
def places(c_id):
        """Get the places by city"""
        the_city = storage.get(City, c_id)
        if the_city is not None:
            return jsonify([a.to_dict() for a in the_city.places])
        abort(404)


@app_views.route('/places/<c_id>', strict_slashes=False, methods=['GET'])
def one_place(c_id):
        """Get place by id"""
        the_place = storage.get(Place, c_id)
        if the_place is not None:
                return jsonify(the_place.to_dict())
        abort(404)


@app_views.route('/places/<c_id>', strict_slashes=False, methods=['DELETE'])
def del_place(c_id):
        """Delete place by id"""
        the_place = storage.get(Place, c_id)
        if the_place is not None:
                storage.delete(the_place)
                storage.save()
                return jsonify({}), 200
        abort(404)


@app_views.route("/cities/<c_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place(c_id):
        """POST a new place on a city"""
        the_city = storage.get(City, c_id)
        if the_city is None:
            abort(404)
        the_json = request.get_json()
        if not the_json:
            abort(400, 'Not a JSON')
        if 'user_id' not in the_json:
            abort(400, 'Missing user_id')
        if 'name' not in the_json:
            abort(400, 'Missing name')
        user_id = request.get_json()["user_id"]
        the_user = storage.get(User, user_id)
        if the_user is None:
            abort(404)
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_place = Place(**request.get_json())
        new_place.city_id = the_city.id
        new_place.user_id = the_user.id
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<c_id>", strict_slashes=False, methods=['PUT'])
def put_place_id(c_id):
        """Update existing place"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        the_place = storage.get(Place, c_id)
        if the_place is not None:
                for attr, value in request.get_json().items():
                    if (hasattr(the_place, attr) and
                            attr != 'id' and attr != 'created_at' and
                            attr != 'updated_at' and attr != 'user_id' and
                            attr != 'city_id'):
                        setattr(the_place, attr, value)
                storage.save()
                return jsonify(the_place.to_dict()), 200
        abort(404)
