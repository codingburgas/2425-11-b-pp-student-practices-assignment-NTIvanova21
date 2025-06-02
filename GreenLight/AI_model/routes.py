from datetime import date

from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
import joblib

from GreenLight.models import Loan, UserLoan
from .logistic_regression_model import features, label_encoders, scaler, model
from .. import db

from . import AI_bp
from .forms import LoanForm


@AI_bp.route('/approvalForm/<int:userId>', methods=['GET', 'POST'])
def approvalForm(userId):

    form = LoanForm()

    today = date.today()
    max_birthdate = today.replace(year=today.year - 18)

    if form.validate_on_submit():
        date_of_birth = form.date_of_birth.data

        if date_of_birth > max_birthdate:
            flash("You must be at least 18 years old to apply for a loan.", "danger")
            return render_template('approvalForm.html', form=form, max_birthdate=max_birthdate.strftime('%Y-%m-%d'))
        else:
            gender = form.gender.data

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

            input_dict = {
                'Gender': gender,
                'Married': marital_status,
                'Dependents': dependents,
                'Education': education,
                'Self_Employed': self_employment,
                'ApplicantIncome': float(applicant_income),
                'CoapplicantIncome': float(coapplicant_income),
                'LoanAmount': float(loan_amount),
                'Loan_Amount_Term': float(loan_term)
            }

            input_processed = []
            for feat in features:
                val = input_dict[feat]
                if feat in label_encoders:
                    val = val.title()
                    val = label_encoders[feat].transform([val])[0]
                input_processed.append(val)

            input_processed = scaler.transform([input_processed])[0]

            probability = model.predict_probability(input_processed)
            prediction = model.predict_class(input_processed)
            approval = "Approved" if prediction == 1 else "Rejected"
            percentage = round(probability * 100, 2)

            loan_form.prediction_result = percentage
            db.session.add(loan_form)
            db.session.commit()

            if percentage >= 50 and percentage <= 100:
                return redirect(url_for('AI.approved', percentage=percentage))
            else:
                return redirect(url_for('AI.disapproved', percentage=percentage))

    return render_template('approvalForm.html', form=form, max_birthdate=max_birthdate.strftime('%Y-%m-%d'))



@AI_bp.route('/approved/<float:percentage>', methods=['GET', 'POST'])
def approved(percentage):
    return render_template("approvedLoanPage.html", current_user=current_user, percentage=percentage)


@AI_bp.route('/disapproved/<float:percentage>', methods=['GET', 'POST'])
def disapproved(percentage):
    return render_template("disapprovedLoanPage.html", current_user=current_user, percentage=percentage)
