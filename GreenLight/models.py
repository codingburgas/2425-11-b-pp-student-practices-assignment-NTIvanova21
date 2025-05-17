from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from GreenLight import db


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column("FirstName", db.String(50))
    middle_name = db.Column("MiddleName",db.String(50))
    last_name = db.Column("LastName",db.String(50))
    email = db.Column("Email",db.String(100), unique=True, nullable=False)
    password = db.Column("Password", db.String(255), nullable=False)
    role = db.Column("Role",db.String(50),nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def id(self):
        return self.userId


class Loan(db.Model):
    __tablename__ = 'Loans'
    __table_args__ = {'extend_existing': True}

    loanId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(50))
    married = db.Column(db.Boolean)
    dependents = db.Column(db.String(50))
    education = db.Column(db.String(50))
    self_employment = db.Column(db.Boolean)
    applicant_income = db.Column(db.Numeric)
    coapplicant_income = db.Column(db.Numeric)
    loan_amount = db.Column(db.Numeric)
    loan_term = db.Column(db.Integer)
    age = db.Column(db.Integer)
    prediction_result = db.Column(db.Boolean)


class UserLoan(db.Model):
    __tablename__ = 'UserLoans'
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), primary_key=True, nullable=False)
    loanId = db.Column(db.Integer, db.ForeignKey('Loans.loanId'), primary_key=True, nullable=False)