from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
from .. import db

from . import auth_bp
from .forms import LoginForm, RegisterForm
from GreenLight.models import User


from .. import login_manager

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))
@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                flash('Invalid password', category='error')
        else:
            flash('Email not found', category='error')
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form, additional_css=url_for('static', filename='auth_base_style.css'))
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('That username is already taken. Please choose another', "error")
            return redirect(url_for('auth.register'))
        else:
            user = User(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()


        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html", form=form, current_user=current_user, additional_css=url_for('static', filename='auth_base_style.css'))
