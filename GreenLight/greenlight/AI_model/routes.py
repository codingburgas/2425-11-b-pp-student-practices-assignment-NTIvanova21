from datetime import date
from flask import render_template, url_for, redirect, flash
from flask_login import current_user
from ..models import Loan, UserLoan
from .. import db
from . import AI_bp
from .forms import LoanForm


from .logistic_regression_model import train_and_evaluate_model


_model_data = None

def get_model_data():
    global _model_data
    if _model_data is None:

        _model_data = train_and_evaluate_model()
    return _model_data

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


        model, scaler, label_encoders, selected_features, accuracy = get_model_data()

        input_data = {
            'Gender': form.gender.data,
            'Married': form.marital_status.data,
            'Dependents': form.dependents.data,
            'Education': form.education.data,
            'Self_Employed': form.self_employment.data,
            'ApplicantIncome': float(form.applicant_income.data),
            'CoapplicantIncome': float(form.coapplicant_income.data),
            'LoanAmount': float(form.loan_amount.data),
            'Loan_Amount_Term': float(form.loan_term.data),
            'Credit_History': float(form.credit_history.data),
            'Property_Area': form.property_area.data
        }


        processed_input = []
        for feature in selected_features:
            value = input_data[feature]
            if feature in label_encoders:
                if isinstance(value, str):
                    value = value.title()
                value = label_encoders[feature].transform([value])[0]
            processed_input.append(value)

        scaled_input = scaler.transform([processed_input])


        probability = model.predict_proba(scaled_input[0])
        percentage = round(probability * 100, 2)


        loan = Loan(
            gender=input_data['Gender'],
            date_of_birth=date_of_birth,
            marital_status=input_data['Married'],
            dependents=input_data['Dependents'],
            education=input_data['Education'],
            self_employment=input_data['Self_Employed'],
            applicant_income=input_data['ApplicantIncome'],
            coapplicant_income=input_data['CoapplicantIncome'],
            loan_amount=input_data['LoanAmount'],
            loan_term=input_data['Loan_Amount_Term'],
            credit_history=input_data['Credit_History'],
            property_area=input_data['Property_Area'],
            prediction_result=percentage
        )

        db.session.add(loan)
        db.session.commit()

        if current_user.is_authenticated:
            user_loan = UserLoan(userId=current_user.id, loanId=loan.loanId)
            db.session.add(user_loan)
            db.session.commit()


        if percentage >= 50:
            return redirect(url_for('AI.approved', percentage=percentage))
        else:
            return redirect(url_for('AI.disapproved', percentage=percentage))

    return render_template('approvalForm.html',
                           form=form,
                           max_birthdate=max_birthdate.strftime('%Y-%m-%d'))


@AI_bp.route('/approved/<float:percentage>', methods=['GET', 'POST'])
def approved(percentage):
    return render_template("approvedLoanPage.html", current_user=current_user, percentage=percentage)


@AI_bp.route('/disapproved/<float:percentage>', methods=['GET', 'POST'])
def disapproved(percentage):
    return render_template("disapprovedLoanPage.html", current_user=current_user, percentage=percentage)
