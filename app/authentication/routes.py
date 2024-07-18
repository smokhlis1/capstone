from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import UserLoginForm
from models import Dueler, db, check_password_hash
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        dueler = Dueler(email=email, password=password)
        db.session.add(dueler)
        db.session.commit()

        flash(f'You have successfully created a dueler account {email}', 'Dueler-Created')
        return redirect(url_for('auth.signin'))

    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        logged_user = Dueler.query.filter_by(email=email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You are now signed in.', 'auth-success')
            return redirect(url_for('site.profile'))
        else:
            flash('Invalid email or password.', 'auth-failed')
            return redirect(url_for('auth.signin'))

    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))