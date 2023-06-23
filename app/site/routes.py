from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user
from models import db, LinkListing, link_schema, links_schema
from forms import LinkSubmissionForm

site = Blueprint('site', __name__, template_folder='site_templates')

# HOME
@site.route('/')
def home():
    return render_template('index.html')

# PROFILE
@site.route('/profile')
def profile():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, query database for their links
        queried_links = LinkListing.query.filter_by(user_id=current_user.id).all()
        # then direct them to profile, passing in necessary data
        return render_template('profile.html', links=queried_links, links_json=links_schema.dump(queried_links))
    else:
        flash('You must be logged in to access the profile page.', category='access-profile-failed')
        return redirect('/signin')

# LINK SUBMISSION
@site.route('/submit', methods=['GET','POST'])
def submit():
    form = LinkSubmissionForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            user_id = current_user.id
            listed_link = form.listed_link.data
            link_title = form.link_title.data
            description = form.description.data
            
            new_link = LinkListing(user_id, listed_link, link_title, description)
            db.session.add(new_link)
            db.session.commit()

            flash(f'Successfully added new link', category='link-submit-success')
            return redirect('/profile')
    except:
        raise Exception('Invalid Form Data')
    return render_template('linksubmission.html', form=form)