from flask import render_template, url_for, redirect, flash, request, current_app
from flask_login import current_user, login_required
from flask_mail import Message

from greenlight.models import UserLoan
from .. import db

from . import main_bp
from ..AI_model.logistic_regression_model import train_and_evaluate_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np

model, scaler, label_encoders, selected_features, accuracy = train_and_evaluate_model()
from ..models import User, Loan
from .. import mail


@main_bp.route('/home')
def home():
    """
        Render the home page, passing the model's accuracy for display.
    """
    return render_template("homePage.html", current_user = current_user, accuracy = accuracy)

@main_bp.route('/show_accounts', methods=['GET', 'POST'])
@login_required
def show_accounts():
    """
        Admin view to list all registered user accounts.
    """
    all_accounts = User.query.all()
    return render_template("adminPage.html", accounts=all_accounts)

@main_bp.route('/activate_account/<int:userId>', methods=['GET', 'POST'])
@login_required
def activate_account(userId):
    """
        Activate a user account by setting isActive = 1 and send email notification.
    """
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
    """
        Deactivate a user account by setting isActive = 0 and send email notification.
    """
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
            flash("Deactivation email sent successfully!", "success")
        except Exception as e:
            print("Error:", e)
            flash("Account activated but email could not be sent.", "warning")

    return redirect(url_for('main.show_accounts'))


@main_bp.route('/change_role/<string:role>/<int:userId>', methods=['GET', 'POST'])
@login_required
def change_role(role, userId):
    """
        Change the role of a user to one of: 'admin', 'customer', or 'bank'.
    """
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
    """
        Permanently delete a user and their associated loans.
    """
    UserLoan.query.filter_by(userId=userId).delete()

    user = User.query.get(userId)
    if user:
        db.session.delete(user)

    db.session.commit()
    flash("Account deleted successfully!", "success")
    return redirect(url_for('main.show_accounts'))
@main_bp.route('/loan_requests', methods=['GET', 'POST'])
@login_required
def loan_requests():
    """
        Bank role view to see all loan requests and the users who submitted them.
    """
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
    """
        Mark a loan request as approved (sets loan.approved = True).
    """
    loan = Loan.query.get(loanId)
    loan.approved = True
    db.session.commit()

    return redirect(url_for('main.loan_requests'))

@main_bp.route('/loan_requests/disapprove/<int:loanId>', methods=['GET', 'POST'])
@login_required
def disapprove_loan_requests(loanId):
    """
        Mark a loan request as disapproved (sets loan.approved = False).
    """
    loan = Loan.query.get(loanId)
    loan.approved = False
    db.session.commit()

    return redirect(url_for('main.loan_requests'))


@main_bp.route('/delete_loan_requests/<int:loanId>', methods=['GET', 'POST'])
@login_required
def delete_loan_requests(loanId):
    """
        Delete a loan and its associated UserLoan relationship.
    """
    loan = Loan.query.get(loanId)

    if loan:
        UserLoan.query.filter_by(loanId=loanId).delete()
        db.session.delete(loan)
        db.session.commit()
        flash("Loan request deleted successfully!", "success")
    return redirect(url_for('main.loan_requests'))

@main_bp.route('/model_metrics')
def model_metrics():
    """
        Display detailed metrics of the logistic regression model.
    """
    # Get model metrics by running evaluation
    from ..AI_model.logistic_regression_model import load_and_prepare_data
    from sklearn.model_selection import train_test_split
    
    # Load and prepare data
    X, y, scaler, label_encoders, selected_features = load_and_prepare_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    # Get predictions
    y_pred = [model.predict_class(x) for x in X_test]
    y_pred_proba = np.array([model.predict_proba(x) for x in X_test])
    
    # Calculate metrics
    accuracy_val = round(accuracy_score(y_test, y_pred) * 100, 2)
    precision_val = round(precision_score(y_test, y_pred) * 100, 2)
    recall_val = round(recall_score(y_test, y_pred) * 100, 2)
    f1_val = round(f1_score(y_test, y_pred) * 100, 2)
    log_loss_val = round(model.calc_loss(y_pred_proba, y_test), 4)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Model parameters
    model_params = {
        'learning_rate': model.learning_rate,
        'threshold': model.threshold,
        'bias': round(model.bias, 4),
        'num_features': len(selected_features),
        'num_weights': len(model.weights)
    }
    
    # Feature importance (using absolute weight values)
    feature_importance = list(zip(selected_features, np.abs(model.weights)))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    return render_template(
        "modelMetricsPage.html",
        accuracy=accuracy_val,
        precision=precision_val,
        recall=recall_val,
        f1_score=f1_val,
        log_loss=log_loss_val,
        confusion_matrix=cm,
        tn=tn, fp=fp, fn=fn, tp=tp,
        model_params=model_params,
        feature_importance=feature_importance,
        selected_features=selected_features
    )







