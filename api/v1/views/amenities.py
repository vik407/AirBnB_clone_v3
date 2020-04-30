#!/usr/bin/python3
"""create a file amenities.py"""
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


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities():
        "Get the amenities"
        return jsonify([a.to_dict() for a in
                       storage.all(Amenity).values()])


@app_views.route('/amenities/<a_id>', strict_slashes=False,
                 methods=['GET'])
def one_amenity(a_id):
        """Get amenity by id"""
        the_amenity = storage.get(Amenity, a_id)
        if the_amenity is not None:
                return jsonify(the_amenity.to_dict())
        abort(404)


@app_views.route('/amenities/<a_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(a_id):
        """Delete amenity by id"""
        the_amenity = storage.get(Amenity, a_id)
        if the_amenity is not None:
                storage.delete(the_amenity)
                storage.save()
                return jsonify({}), 200
        abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def post_amenity():
        """POST a new amenity"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        if 'name' not in the_json:
                abort(400, 'Missing name')
        new_amenity = Amenity(**request.get_json())
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<a_id>", strict_slashes=False, methods=['PUT'])
def put_amenity_id(a_id):
        """Update existing amenity"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        the_amenity = storage.get(Amenity, a_id)
        if the_amenity is not None:
                for attr, value in request.get_json().items():
                    if (hasattr(the_amenity, attr) and
                            attr != 'id' and attr != 'created_at' and
                            attr != 'updated_at'):
                        setattr(the_amenity, attr, value)
                storage.save()
                return jsonify(the_amenity.to_dict()), 200
        abort(404)
