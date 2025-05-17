from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from .. import db

from . import profile_bp
from GreenLight.models import User
from .. import login_manager

@profile_bp.route('/profile/<int:userId>', methods=['GET', 'POST'])
@login_required
def profile(userId):
    user = User.query.get(userId)
    return render_template("profilePage.html", user=user)

@profile_bp.route('/edit_profile/<int:userId>', methods=['GET', 'POST'])
@login_required
def edit_profile(userId):
    user = User.query.get(userId)

    return render_template("profilePage.html", user=user)

