#!/usr/bin/python3
"""create a file states.py"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
        "Get the states"
        return jsonify([state.to_dict() for state in
                       storage.all(State).values()])


@app_views.route('/states/<s_id>', strict_slashes=False,
                 methods=['GET'])
def one_state(s_id):
        """Get state by id"""
        the_state = storage.get(State, s_id)
        if the_state is not None:
                return jsonify(the_state.to_dict())
        abort(404)


@app_views.route('/states/<s_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(s_id):
        """Delete state by id"""
        the_state = storage.get(State, s_id)
        if the_state is not None:
                storage.delete(the_state)
                storage.save()
                return jsonify({}), 200
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_state():
        """POST a new state"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        if 'name' not in the_json:
                abort(400, 'Missing name')
        new_state = State(**request.get_json())
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<s_id>", strict_slashes=False, methods=['PUT'])
def put_state_id(s_id):
        """Update existing state"""
        the_json = request.get_json()
        if not the_json:
                abort(400, 'Not a JSON')
        the_state = storage.get(State, s_id)
        if the_state is not None:
                for attr, value in request.get_json().items():
                        setattr(the_state, attr, value)
                storage.save()
                return jsonify(the_state.to_dict()), 200
        abort(404)
