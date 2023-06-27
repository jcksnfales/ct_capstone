from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, LinkListing, link_schema, links_schema

api = Blueprint('api',__name__, url_prefix='/api')

# INFO PAGE
@api.route('/info')
def info():
    return render_template('apidocs.html')


#### CREATE

# CREATE NEW LINK
@api.route('/submit', methods=['POST'])
@token_required
def create(token_user):
    # initialize new link listing
    new_link = LinkListing(token_user.id, request.json['listed_link'], request.json['link_title'], request.json['description'], request.json['is_public'])
    # add link listing to database
    db.session.add(new_link)
    db.session.commit()
    # return link info to user to confirm addition
    return jsonify({'message': 'Link successfully added'}, link_schema.dump(new_link))


#### READ

# GET ALL PUBLIC LINKS
@api.route('/get/all', methods=['GET'])
@token_required
def get_all(token_user):
    queried_links = LinkListing.query.filter_by(is_public=True).all()
    return jsonify(links_schema.dump(queried_links))

# GET PERSONAL LINKS
@api.route('/get/mine', methods=['GET'])
@token_required
def get_personal(token_user):
    queried_links = LinkListing.query.filter_by(user_id=token_user.id).all()
    return jsonify(links_schema.dump(queried_links))

# GET ALL LINKS BY USER
@api.route('/get/user/<user_id>', methods=['GET'])
@token_required
def get_user(token_user, user_id):
    # only give token user results they are permitted to see
    if token_user.id == user_id:
        # if matched, give all results
        queried_links = LinkListing.query.filter_by(user_id=user_id).all()
    else:
        # if not matched, give only public results
        queried_links = LinkListing.query.filter_by(user_id=user_id, is_public=True).all()
    return jsonify(links_schema.dump(queried_links))

# GET LINK BY ID
@api.route('/get/link/<link_id>', methods=['GET'])
@token_required
def get_link(token_user, link_id):
    queried_link = LinkListing.query.get(link_id)
    # if link doesn't exist, return an error message
    if not queried_link:
        return jsonify({'message': 'Invalid link ID'})
    # only give token user the result if they are permitted to see (listing either owned by them or public)
    if token_user.id == queried_link.user_id or queried_link.is_public:
        return jsonify(link_schema.dump(queried_link))
    else:
        return jsonify({'message': 'Invalid link ID'})
        

#### UPDATE

# UPDATE LINK BY ID
@api.route('/update/<link_id>', methods=['POST','PUT'])
@token_required
def update(token_user, link_id):
    # query for listing to be updated
    updated_link = LinkListing.query.get(link_id)
    # if listing does not exist, return an error message
    if not updated_link:
        return jsonify({'message': 'Invalid link ID'})
    # check if token user is permitted to update this listing
    if token_user.id == updated_link.user_id:
        # if listing owned by token user, try updating values with given JSON data
        try:
            # check value type for 'listed_link' field (must be string)
            if isinstance(request.json['listed_link'], str):
                updated_link.listed_link = request.json['listed_link']
            else:
                return jsonify({'message': 'Key listed_link must have string value'})
            # check value type for 'link_title' field (must be string)
            if isinstance(request.json['link_title'], str):
                updated_link.link_title = request.json['link_title']
            else:
                return jsonify({'message': 'Key link_title must have string value'})
            # check value type for 'description' field (must be string)
            if isinstance(request.json['description'], str):
                updated_link.description = request.json['description']
            else:
                return jsonify({'message': 'Key description must have string value'})
            # check value type for 'is_public' field (must be boolean)
            if isinstance(request.json['is_public'], bool):
                updated_link.is_public = request.json['is_public']
            else:
                return jsonify({'message': 'Key is_public must have boolean value'})
        except KeyError:
            # if a field is not found, return error message
            return jsonify({'message': 'JSON key error (are you missing a field?)'})
        # commit changes to database
        db.session.commit()
        # return new listing info to user to confirm update
        return jsonify({'message': 'Link successfully updated'}, link_schema.dump(updated_link))
    else:
        # if listing not owned by token user, return error message
        return jsonify({'message': 'Invalid link ID'})


#### DELETE

# DELETE BY ID
@api.route('/delete/<link_id>', methods=['DELETE'])
@token_required
def delete(token_user, link_id):
    # query for listing to be deleted
    deleted_link = LinkListing.query.get(link_id)
    # if listing does not exist, return an error message
    if not deleted_link:
        return jsonify({'message': 'Invalid link ID'})
    # check if token user is permitted to delete this listing
    if token_user.id == deleted_link.user_id:
        # if listing owned by token user, delete listing and commit change to database
        db.session.delete(deleted_link)
        db.session.commit()
        # return confirmation message to user
        return jsonify({'message': 'Link successfully deleted'}, link_schema.dump(deleted_link))
    else:
        # if listing not owned by token user, return error message
        return jsonify({'message': 'Invalid link ID'})