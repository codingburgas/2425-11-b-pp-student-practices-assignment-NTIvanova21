from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user

from models import Loan, UserLoan
from .. import db

from . import AI_bp
from .forms import LoanForm


@AI_bp.route('/approvalForm/<int:userId>', methods=['GET', 'POST'])
def approvalForm(userId):

    form = LoanForm()

    if form.validate_on_submit():
        gender = form.gender.data
        date_of_birth = form.date_of_birth.data
        marital_status = form.marital_status.data
        dependents = form.dependents.data
        education = form.education.data
        self_employment = form.self_employment.data
        applicant_income = form.applicant_income.data
        coapplicant_income = form.coapplicant_income.data
        loan_amount = form.loan_amount.data
        loan_term = form.loan_term.data

        loan_form = Loan(gender = gender, date_of_birth = date_of_birth,  marital_status = marital_status, dependents = dependents, education = education, self_employment = self_employment, applicant_income = applicant_income, coapplicant_income = coapplicant_income, loan_amount = loan_amount, loan_term = loan_term)

        db.session.add(loan_form)
        db.session.commit()

        userLoan = UserLoan(userId=userId, loanId=loan_form.loanId)
        db.session.add(userLoan)
        db.session.commit()

        flash('Form submitted successfully!', 'success')
        return redirect(url_for('AI.approvalForm', userId=userId))



    return render_template('approvalForm.html', form=form)

