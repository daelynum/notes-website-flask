from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # on the login page we get the user's mail and password
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # find a user in the DB by email (it is unique)
        user = User.query.filter_by(email=email).first()
        if user:
            # pass checking
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')

                login_user(user, remember=True)
                # if login and password are correct, redirect to home page
                return redirect(url_for('views.home'))
            # added the ability to login to users created by the admin
            # (until I figure out hashing when creating a password by an admin)
            elif user.password == password:
                flash('Logged in successfully!', category='success')

                login_user(user, remember=True)
                # if login and password are correct, redirect to home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # error output for users

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # if everything is correct, a new user is created
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


# rout for Logout button
@auth.route('/logout')
# it will ensure that the current user is logged in and authenticated before calling the actual view
@login_required
def logout():
    #  This function will also clean up the remember cookie if it exists.
    logout_user()
    return redirect(url_for('auth.login'))
