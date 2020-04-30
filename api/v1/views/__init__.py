#!/usr/bin/python3
"""create a variable app_views which is an instance of Blueprint"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.states import *
from api.v1.views.cities import *


def get(data):
    """For GET requests"""
    if data['p_id']:
        parent = storage.get(data['p_str'], data['p_id'])
        if parent:
            return jsonify([p.to_dict() for p in
                           getattr(parent, data['p_child'])]), 200
        abort(404)
    if data['_id']:
        found = storage.get(data['str'], data['_id'])
        if found:
            return jsonify(found.to_dict()), 200
        abort(404)
    else:
        return jsonify([notfound.to_dict() for notfound in
                       storage.all(data['str']).values()]), 200


def delete(data):
    """For DELETE requests"""
    found = storage.get(data['str'], data['_id'])
    if found:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


def post(data):
    """For POST requests"""
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    for c in data['check']:
        if c not in req:
            return jsonify({'error': 'Missing {}'.format(c)}), 400
    if data['p_id']:
        if 'user_id' in data['check']:
            if not storage.get('User', req['user_id']):
                abort(404)
        parent = storage.get(data['p_str'], data['p_id'])
        if parent:
            req[data['p_prop']] = data['p_id']
            new = eval(data['str'])(**req)
            new.save()
            return jsonify(new.to_dict()), 201
        abort(404)
    new = eval(data['str'])(**req)
    new.save()
    return jsonify(new.to_dict()), 201


def put(data):
    """For PUT requests"""
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    found = storage.get(data['str'], data['_id'])
    if found:
        for k, v in req.items():
            if k not in data['ignore']:
                setattr(found, k, v)
        storage.save()
        return jsonify(found.to_dict()), 200
    else:
        abort(404)
