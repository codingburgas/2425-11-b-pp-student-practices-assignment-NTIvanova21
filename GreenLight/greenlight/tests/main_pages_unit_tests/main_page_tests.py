import unittest
from greenlight import create_app, db
from greenlight.models import User, UserLoan, Loan

class TestConfig:
    """Configuration class for test environment."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@localhost/TestDatabase?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    WTF_CSRF_ENABLED = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'greenlightsystem123@gmail.com'
    MAIL_PASSWORD = 'qnlmdlvcncqfshqu'
    MAIL_USE_TLS = True


class MainRoutesTestCase(unittest.TestCase):
    """Test suite for admin-related routes in the main blueprint."""
    def setUp(self):
        """Create app, context, test client, and an admin user."""

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create and login as admin user
        self.admin_user = User(
            first_name='Admin',
            middle_name='Middle',
            last_name='User',
            email='admin@test.com',
            password='123',
            role='admin',
            isActive=True,
            profilePicture='default.svg'
        )
        self.admin_user.set_password('password')
        db.session.add(self.admin_user)
        db.session.commit()

        self.client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'password'
        }, follow_redirects=True)

    def tearDown(self):
        """Clear session and drop database after each test."""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test that home page loads correctly."""
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'accuracy', response.data.lower())

    def test_show_accounts(self):
        """Test that accounts list displays registered users."""

        response = self.client.get('/show_accounts')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'admin@test.com', response.data)

    def test_activate_account(self):
        """Test activating a deactivated user account."""

        user = User(
            email='inactive@test.com',
            isActive=False,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/activate_account/{user.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_user = User.query.get(user.id)
        self.assertTrue(updated_user.isActive)

    def test_deactivate_account(self):
        """Test deactivating an active user account."""

        user = User(
            email='active@test.com',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/deactivate_account/{user.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_user = User.query.get(user.id)
        self.assertFalse(updated_user.isActive)

    def test_change_role(self):
        """Test changing a user's role from customer to admin."""
        user = User(
            email='changerole@test.com',
            role='customer',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/change_role/admin/{user.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.get(user.id).role, 'admin')

    def test_delete_account(self):
        """Test deleting a user account."""
        user = User(
            email='delete@test.com',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/delete_account/{user.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(User.query.get(user.id))

    def test_loan_requests_page(self):
        """Test loan requests page loads and displays loan entries."""
        user = User(
            email='loanuser@test.com',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        loan = Loan(approved=False)
        db.session.add(loan)
        db.session.commit()

        user_loan = UserLoan(userId=user.userId, loanId=loan.loanId)
        db.session.add(user_loan)
        db.session.commit()

        response = self.client.get('/loan_requests')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'loan', response.data.lower())

    def test_approve_loan(self):
        """Test approving a pending loan request."""
        user = User(
            email='loanuser@test.com',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        loan = Loan(approved=False)
        db.session.add(loan)
        db.session.commit()

        user_loan = UserLoan(userId=user.userId, loanId=loan.loanId)
        db.session.add(user_loan)
        db.session.commit()

        response = self.client.post(f'/loan_requests/approve/{loan.loanId}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_loan = Loan.query.filter_by(loanId=loan.loanId).first()
        self.assertTrue(updated_loan.approved)

    def test_disapprove_loan(self):
        """Test disapproving an already approved loan."""

        user = User(
            email='loanuser@test.com',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        loan = Loan(approved=True)
        db.session.add(loan)
        db.session.commit()

        user_loan = UserLoan(userId=user.userId, loanId=loan.loanId)
        db.session.add(user_loan)
        db.session.commit()

        response = self.client.post(f'/loan_requests/disapprove/{loan.loanId}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_loan = Loan.query.filter_by(loanId=loan.loanId).first()
        self.assertFalse(updated_loan.approved)

    def test_delete_loan_request(self):
        """Test deletion of a loan request."""
        user = User(
            email='loanuser@test.com',
            isActive=True,
            password='pass',
            profilePicture='default.svg'
        )
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        loan = Loan(approved=False)
        db.session.add(loan)
        db.session.commit()

        user_loan = UserLoan(userId=user.userId, loanId=loan.loanId)
        db.session.add(user_loan)
        db.session.commit()

        response = self.client.post(f'/delete_loan_requests/{loan.loanId}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        deleted_loan = Loan.query.filter_by(loanId=loan.loanId).first()
        self.assertIsNone(deleted_loan)