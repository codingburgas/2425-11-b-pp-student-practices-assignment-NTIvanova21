from flask import render_template, url_for, redirect, flash, current_app
from flask_login import login_user, logout_user, current_user
from flask_mail import Message

from .. import db, mail

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
                if user.role == 'admin':
                    return redirect(url_for('main.show_accounts'))
                elif user.role == 'customer':
                    return redirect(url_for('main.home'))
                if user.role == 'bank':
                    return redirect(url_for('main.loan_requests'))
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
        try:
            msg = Message(subject='Created account',
                          body="Your account was successfully created! The admin will soon activate your account! This is automatically generated message. Please, don't reply!",
                          recipients=[user.email], sender=current_app.config['MAIL_USERNAME'])

            mail.send(msg)
        except Exception as e:
            print("Error:", e)
        flash('Account created! Wait for account activation', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html", form=form, current_user=current_user, additional_css=url_for('static', filename='auth_base_style.css'))
