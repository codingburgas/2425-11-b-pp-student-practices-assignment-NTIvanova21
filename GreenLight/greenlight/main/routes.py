from flask import render_template, url_for, redirect, flash, request, current_app
from flask_login import current_user, login_required
from flask_mail import Message

from greenlight.models import UserLoan
from .. import db

from . import main_bp
from ..AI_model.logistic_regression_model import train_and_evaluate_model

model, scaler, label_encoders, selected_features, accuracy = train_and_evaluate_model()
from ..models import User, Loan
from .. import mail


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
        try:
            msg = Message(subject='Activated account',
                          body="Your account was successfully activated! This is automatically generated message. Please, don't reply!",
                          recipients=[user.email], sender=current_app.config['MAIL_USERNAME'])

            mail.send(msg)
            flash("Activation email sent successfully!", "success")
        except Exception as e:
            print("Error:", e)
            flash("Account activated but email could not be sent.", "warning")

    return redirect(url_for('main.show_accounts'))

@main_bp.route('/deactivate_account/<int:userId>', methods=['GET', 'POST'])
@login_required
def deactivate_account(userId):
    if request.method == 'POST':
        user = User.query.get(userId)
        if user:
            user.isActive = 0
            db.session.commit()
        try:
            msg = Message(subject='Deactivated account',
                          body="Your account was successfully deactivated! This is automatically generated message. Please, don't reply!",
                          recipients=[user.email], sender=current_app.config['MAIL_USERNAME'])

            mail.send(msg)
            flash("Activation email sent successfully!", "success")
        except Exception as e:
            print("Error:", e)
            flash("Account activated but email could not be sent.", "warning")

    return redirect(url_for('main.show_accounts'))


@main_bp.route('/change_role/<string:role>/<int:userId>', methods=['GET', 'POST'])
@login_required
def change_role(role, userId):
    if request.method == 'GET':
        user = User.query.get(userId)
        if user and role in ['admin', 'customer', 'bank']:
            if role == 'admin':
                user.role = 'admin'
                db.session.commit()
            if role == 'customer':
                user.role = 'customer'
                db.session.commit()
            if role == 'bank':
                user.role = 'bank'
                db.session.commit()
            flash("Role was changed successfully!", "success")
        else:
            flash('Error')


    return redirect(url_for('main.show_accounts'))

@main_bp.route('/delete_account/<int:userId>', methods=['GET', 'POST'])
@login_required
def delete_account(userId):
    user = User.query.get(userId)
    user_loans = UserLoan.query.all()
    db.session.delete(user)

    if userId in user_loans:
        user_loans.delete(userId)
    db.session.commit()

    return redirect(url_for('main.show_accounts'))
@main_bp.route('/loan_requests', methods=['GET', 'POST'])
@login_required
def loan_requests():
    db.session.expire_all()
    user_loans = UserLoan.query.all()
    users_with_loans = []

    for user_loan in user_loans:
        user = User.query.get(user_loan.userId)
        loan = Loan.query.get(user_loan.loanId)
        if user and loan:
            users_with_loans.append({
                "user": user,
                "loan": loan
            })

    return render_template('bankLoanRequestPage.html',current_user=current_user,users_with_loans=users_with_loans)
@main_bp.route('/loan_requests/approve/<int:loanId>', methods=['GET', 'POST'])
@login_required
def approve_loan_requests(loanId):
    loan = Loan.query.get(loanId)
    loan.approved = True
    db.session.commit()

    return redirect(url_for('main.loan_requests'))

@main_bp.route('/loan_requests/disapprove/<int:loanId>', methods=['GET', 'POST'])
@login_required
def disapprove_loan_requests(loanId):
    loan = Loan.query.get(loanId)
    loan.approved = False
    db.session.commit()

    return redirect(url_for('main.loan_requests'))


@main_bp.route('/delete_loan_requests/<int:loanId>', methods=['GET', 'POST'])
@login_required
def delete_loan_requests(loanId):
    loan = Loan.query.get(loanId)

    if loan:
        UserLoan.query.filter_by(loanId=loanId).delete()
        db.session.delete(loan)
        db.session.commit()

    return redirect(url_for('main.loan_requests'))







