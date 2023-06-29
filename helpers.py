from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal
from models import User, LinkListing, db

def count_public_links(user_id):
    user_public_listings = len(LinkListing.query.filter_by(user_id=user_id, is_public=True).all())
    updated_user = User.query.get(user_id)
    updated_user.public_link_count = user_public_listings
    db.session.commit()

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