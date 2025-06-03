from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from .. import db

from . import main_bp
from GreenLight.models import User, Loan
from .. import login_manager
from GreenLight.AI_model.logistic_regression_model import accuracy
@main_bp.route('/home')
def home():
    return render_template("homePage.html", current_user = current_user, accuracy = accuracy)

@main_bp.route('/show_accounts', methods=['GET', 'POST'])
@login_required
def show_accounts():
    all_accounts = User.query.all()
    return render_template("adminPage.html", accounts=all_accounts)

@main_bp.route('/activate_account/<int:userId>', methods=['GET', 'POST'])
@login_required
def activate_account(userId):
    if request.method == 'POST':
        user = User.query.get(userId)
        if user:
            user.isActive = 1
            db.session.commit()

    return redirect(url_for('main.show_accounts'))

@main_bp.route('/deactivate_account/<int:userId>', methods=['GET', 'POST'])
@login_required
def deactivate_account(userId):
    if request.method == 'POST':
        user = User.query.get(userId)
        if user:
            user.isActive = 0
            db.session.commit()

    return redirect(url_for('main.show_accounts'))


@main_bp.route('/change_role/<string:role>/<int:userId>', methods=['GET', 'POST'])
@login_required
def change_role(role, userId):
    if request.method == 'GET':
        user = User.query.get(userId)
        if user and role in ['admin', 'customer']:
            if role == 'admin':
                user.role = 'admin'
                db.session.commit()
            if role == 'customer':
                user.role = 'customer'
                db.session.commit()
        else:
            flash('Error')


    return redirect(url_for('main.show_accounts'))

@main_bp.route('/loan_requests', methods=['GET', 'POST'])
@login_required
def loan_requests():
    loans = Loan.query.all()
    return render_template('bankLoanRequestPage.html',current_user = current_user, loans = loans)

@main_bp.route('/loan_requests/<int:loanId>', methods=['GET', 'POST'])
@login_required
def approve_loan_requests(loanId):
    loan = Loan.query.get(loanId)
    loans = Loan.query.all()
    loan.approved = True
    db.session.commit()

    return render_template('bankLoanRequestPage.html',loans = loans)

