#!/usr/bin/python3
"""create a file places_amenities.py"""
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


@app_views.route('/places/<p_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenities(p_id):
        """Get the amenities by place"""
        the_amenity = storage.get(Place, p_id)
        if the_amenity is not None:
            return jsonify([a.to_dict() for a in the_amenity.amenities])
        abort(404)


@app_views.route('/places/<p_id>/amenities/<a_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place_amenity(p_id, a_id):
        """Delete amenity by place and amenity id"""
        the_place = storage.get(Place, p_id)
        if the_place is not None:
            the_amenity = storage.get(Amenity, a_id)
            if the_amenity is not None:
                    storage.delete(the_amenity)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
        abort(404)


@app_views.route("/places/<p_id>/amenities/<a_id>", strict_slashes=False,
                 methods=['POST'])
def post_place_amenity(p_id, a_id):
        """POST a new amenity on a place"""
        the_place = storage.get(Place, p_id)
        if the_place is not None:
            the_amenity = storage.get(Amenity, a_id)
            if the_amenity is not None:
                place_amenity = the_place.amenities
                if the_amenity in place_amenity:
                    return jsonify(the_amenity.to_dict(), 200)
                place_amenity.append(the_amenity)
            abort(404)
        abort(404)
