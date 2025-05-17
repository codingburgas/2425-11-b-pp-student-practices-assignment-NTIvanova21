from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from .. import db

from . import main_bp
from GreenLight.models import User


from .. import login_manager

@main_bp.route('/home')
def home():
    return render_template("homePage.html")

@main_bp.route('/show_accounts', methods=['GET', 'POST'])
@login_required
def show_accounts():
    all_accounts = User.query.all()
    return render_template("adminPage.html", accounts=all_accounts)
