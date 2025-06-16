from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """
        Login form for existing users.

        Fields:
            - email: User's email address (required)
            - password: User's password (required)
            - submit: Button to submit the form
    """
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    """
        Registration form for new users.

        Fields:
            - first_name: User's first name (required)
            - middle_name: User's middle name (required)
            - last_name: User's last name (required)
            - email: User's email address (required)
            - password: Desired password (required)
            - submit: Button to submit the form
    """
    first_name = StringField('first name', validators=[DataRequired()])
    middle_name = StringField('middle name', validators=[DataRequired()])
    last_name = StringField('last name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign up')