from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user
from models import db, User, LinkListing, link_schema, links_schema
from forms import LinkSubmissionForm

site = Blueprint('site', __name__, template_folder='site_templates')

# HOME
@site.route('/')
def home():
    return render_template('index.html')

# USERS LIST
@site.route('/users/all')
def catalog():
    users = User.query.filter(User.public_link_count > 0).all()

    return render_template('userlist.html', users=users)

# USER PAGE
@site.route('/users/<id>')
def userpage(id):
    # query database for public links by this user
    queried_links = LinkListing.query.filter_by(user_id=id, is_public=True).all()
    # query database for user info
    queried_user = User.query.get(id)

    return render_template('userpage.html', links=queried_links, user=queried_user)

# PROFILE
@site.route('/profile')
def profile():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, query database for their links
        queried_links = LinkListing.query.filter_by(user_id=current_user.id).all()
        # then direct them to profile, passing in necessary data
        return render_template('profile.html', links=queried_links)
    else:
        flash('You must be logged in to access the profile page.', category='access-profile-failed')
        return redirect('/signin')

# LINK SUBMISSION
@site.route('/submit', methods=['GET','POST'])
def submit():
    form = LinkSubmissionForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            # add new link listing
            user_id = current_user.id
            listed_link = form.listed_link.data
            link_title = form.link_title.data
            description = form.description.data
            is_public = form.is_public.data
            
            new_link = LinkListing(user_id, listed_link, link_title, description, is_public)
            db.session.add(new_link)

            # commit changes to database
            db.session.commit()

            # TODO update user's public link count

            # flash success message
            flash(f'Successfully added new links', category='link-submit-success')
            return redirect('/profile')
    except:
        raise Exception('Invalid Form Data')
    return render_template('linksubmission.html', form=form)

# LINK EDITING
@site.route('/update/<link_id>', methods=['GET','POST'])
def update(link_id):
    form = LinkSubmissionForm()
    updated_link = LinkListing.query.get(link_id)
    
    # check if user owns this listing
    if current_user.id != updated_link.user_id:
        # if not, flash error message and redirect to profile
        flash(f'Either you are not authorized to edit that link, or it does not exist.', category='link-edit-failed')
        return redirect('/profile')

    try:
        if request.method == 'POST' and form.validate_on_submit():
            # update listing data
            updated_link.listed_link = form.listed_link.data
            updated_link.link_title = form.link_title.data
            updated_link.description = form.description.data
            updated_link.is_public = form.is_public.data

            # commit changes to database
            db.session.commit()

            # TODO update user's public link count

            # flash success message and redirect back to profile
            flash(f'Successfully edited link', category='link-submit-success')
            return redirect('/profile')
    except:
        raise Exception('Invalid Form Data')
    
    return render_template('linkupdate.html', form=form, listing_data=updated_link)

# LINK DELETION
@site.route('/delete/<id>')
def delete(id):
    deleted_listing = LinkListing.query.get(id)

    # check if user is authorized to delete this listing
    if current_user.id == deleted_listing.user_id:
        # delete link listing
        db.session.delete(deleted_listing)

        # commit changes to database
        db.session.commit()

        # TODO update user's public link count

        # flash success message
        flash(f'Successfully deleted link.', category='link-delete-success')
    else:
        flash(f'Either you are not authorized to delete that link, or it does not exist.', category='link-delete-failed')
    return redirect('/profile')