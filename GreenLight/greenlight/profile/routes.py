from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db

from . import profile_bp
from ..models import User
from .. import login_manager

@profile_bp.route('/profile/<int:userId>', methods=['GET', 'POST'])
@login_required
def profile(userId):
    if current_user.userId != userId:
        abort(500)
    user = User.query.get(userId)
    return render_template("profilePage.html", user=user)

@profile_bp.route('/change_profile_picture/<int:userId>/<string:profilePicture>', methods=['GET', 'POST'])
@login_required
def change_profile_picture(userId, profilePicture):
    if current_user.userId != userId:
        abort(500)
    user = User.query.get(userId)
    user.profilePicture = profilePicture
    db.session.commit()

    return redirect(url_for('profile.profile', userId=userId, profilePicture = profilePicture))

@profile_bp.route('/change_password/<int:userId>', methods=['POST'])
@login_required
def change_password(userId):
    if current_user.userId != userId:
        abort(500)

    user = User.query.get(userId)
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not check_password_hash(user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for('profile.profile', userId=userId))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('profile.profile', userId=userId))

    user.password = generate_password_hash(new_password)
    db.session.commit()
    flash("Password was successfully changed!", "success")
    return redirect(url_for('profile.profile', userId=userId))




