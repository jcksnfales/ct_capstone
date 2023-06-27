from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None
        
        try:
            token = request.headers['x-access-token'].split(' ')[1]
        except:
            return jsonify({'message': 'Token error'})

        try:
            token_user = User.query.filter_by(token = token).first()
            print(token, token_user)
        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token invalid'})
        return our_flask_function(token_user, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)