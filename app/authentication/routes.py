from forms import UserLoginForm, UserRegisterForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# SIGN UP
@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserRegisterForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # find existing users' emails with a database query
            existing_users = [e[0] for e in db.session.query(User.email).all()]
            # then, check entered email against existing emails
            if email in existing_users:
                # if there's already an account registered with that email, return the user an error
                flash(f'"{email}" has already been registered.', category='auth-register-failed')
                return redirect('/signup')
            else:
                # otherwise, register the email
                new_user = User(email, password=password)
                db.session.add(new_user)
                db.session.commit()

                flash(f'Successfully registered "{email}"', category='auth-register-success')
                return redirect('/signin')
    except:
        raise Exception('Invalid Form Data')
    return render_template('sign_up.html', form=form)

# SIGN IN
@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # query the database for the given user's record
            logged_user = User.query.filter(User.email == email).first()
            # check if there is an existing record for the given user, and check the given password against the recorded one
            if logged_user and check_password_hash(logged_user.password, password):
                # if the username and password are valid, log user in and return a success message
                login_user(logged_user)
                flash('Successfully logged in.', 'auth-login-success')
                return redirect('/profile')
            else:
                # if the username/password are NOT valid, return the user an error message
                flash('Incorrect username or password.', category='auth-login-failed')
                return redirect('/signin')
    except:
        raise Exception('Invalid Form Data')
    return render_template('sign_in.html', form=form)

# LOG OUT
@auth.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out.', 'auth-logout-success')
    return redirect('/signin')