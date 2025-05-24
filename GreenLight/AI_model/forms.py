from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, InputRequired

class LoanForm(FlaskForm):
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()],coerce=str)
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    marital_status = RadioField('Marital Status',choices=[('yes', 'Yes'), ('no', 'No')],validators=[InputRequired()],coerce=str)
    dependents = SelectField('Number of Dependents',choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3+', '3 or more')],validators=[InputRequired()])
    education = RadioField('Education',choices=[('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')],validators=[InputRequired()],coerce=str, render_kw={"class": "form-check-input"})
    self_employment = RadioField('Self_employment',choices=[('yes', 'Yes'), ('no', 'No')],validators=[InputRequired()],coerce=str)
    applicant_income = StringField('Applicant Income', validators=[DataRequired()])
    coapplicant_income = StringField('Coapplicant Income', validators=[DataRequired()])
    loan_amount = StringField('Loan Amount', validators=[DataRequired()])
    loan_term = RadioField('Loan Term',choices=[('6', '6 months'),('12', '12 months'),('36', '36 months'),('36', '3 years'),('60', '5 years')],validators=[InputRequired()],coerce=str)
    submit = SubmitField('Check Eligibility')
