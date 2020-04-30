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


@app_views.route('/places/<p_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def reviews(p_id):
        """Get the reviews by place"""
        the_review = storage.get(Place, p_id)
        if the_review is not None:
            return jsonify([a.to_dict() for a in the_review.reviews])
        abort(404)


@app_views.route('/reviews/<p_id>', strict_slashes=False, methods=['GET'])
def one_review(p_id):
        """Get reviews by id"""
        the_review = storage.get(Review, p_id)
        if the_review is not None:
                return jsonify(the_review.to_dict())
        abort(404)


@app_views.route('/reviews/<p_id>', strict_slashes=False, methods=['DELETE'])
def del_review(p_id):
        """Delete review by id"""
        the_review = storage.get(Review, p_id)
        if the_review is not None:
                storage.delete(the_review)
                storage.save()
                return jsonify({}), 200
        abort(404)


@app_views.route("/places/<p_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(p_id):
        """POST a new review on a place"""
        the_place = storage.get(Place, p_id)
        if the_place is None:
            abort(404)
        the_json = request.get_json()
        if not the_json:
            abort(400, 'Not a JSON')
        if 'user_id' not in the_json:
            abort(400, 'Missing user_id')
        user_id = request.get_json()["user_id"]
        the_user = storage.get(User, user_id)
        if the_user is None:
            abort(404)
        if 'text' not in the_json:
            abort(400, 'Missing text')
        new_review = Review(**request.get_json())
        new_review.place_id = the_place.id
        new_review.user_id = the_user.id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<p_id>", strict_slashes=False, methods=['PUT'])
def put_review_id(p_id):
        """Update existing review"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        the_review = storage.get(Review, p_id)
        if the_review is not None:
                for attr, value in request.get_json().items():
                    if (hasattr(the_review, attr) and
                            attr != 'id' and attr != 'created_at' and
                            attr != 'updated_at' and attr != 'user_id' and
                            attr != 'place_id'):
                        setattr(the_review, attr, value)
                storage.save()
                return jsonify(the_review.to_dict()), 200
        abort(404)
