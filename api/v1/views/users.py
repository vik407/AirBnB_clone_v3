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


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users():
        "Get the users"
        return jsonify([a.to_dict() for a in
                       storage.all(User).values()])


@app_views.route('/users/<u_id>', strict_slashes=False,
                 methods=['GET'])
def one_user(u_id):
        """Get user by id"""
        the_user = storage.get(User, u_id)
        if the_user is not None:
                return jsonify(the_user.to_dict())
        abort(404)


@app_views.route('/users/<u_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_user(u_id):
        """Delete user by id"""
        the_user = storage.get(User, u_id)
        if the_user is not None:
                storage.delete(the_user)
                storage.save()
                return jsonify({}), 200
        abort(404)


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
        """POST a new user"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        if 'email' not in the_json:
                abort(400, 'Missing email')
        if 'password' not in the_json:
                abort(400, 'Missing password')
        new_user = User(**request.get_json())
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<u_id>", strict_slashes=False, methods=['PUT'])
def put_user_id(u_id):
        """Update existing user"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        the_user = storage.get(User, u_id)
        if the_user is not None:
                for attr, value in request.get_json().items():
                    if (hasattr(the_user, attr) and
                            attr != 'id' and attr != 'created_at' and
                            attr != 'updated_at') and attr != 'email':
                        setattr(the_user, attr, value)
                storage.save()
                return jsonify(the_user.to_dict()), 200
        abort(404)
