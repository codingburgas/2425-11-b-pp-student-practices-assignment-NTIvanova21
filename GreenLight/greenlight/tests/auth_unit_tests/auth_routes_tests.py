import dotenv
from greenlight.models import User

dotenv.load_dotenv("settings.env")
import unittest
from greenlight import create_app, db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@localhost/TestDatabase?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    WTF_CSRF_ENABLED = False



class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_redirects_to_login_page(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])
        if response.status_code == 200:
            print("Index redirected to login")
        else:
            print(f"Unexpected status code: {response.status_code}")

    def test_register_user(self):
        response = self.client.post('/register', data={
            'first_name': 'John',
            'middle_name': 'Doe',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'password': 'pass1234',
            'confirm_password': 'pass1234'
        }, follow_redirects=True)


        if response.status_code == 200:
            print("User registration request successful - user should be registered.")
        else:
            print(f"Unexpected status code: {response.status_code}")

        self.assertIn(b'Account created', response.data)

    def test_login_success(self):
        with self.app.app_context():
            user = User(first_name='John', last_name='Smith', email='test@example.com', role='customer', isActive=True)
            user.set_password('pass1234')
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'pass1234'
        }, follow_redirects=True)

        if response.status_code == 200:
            print("Login successful - user should be logged in.")
        else:
            print(f"Unexpected status code: {response.status_code}")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'login', response.data)

    def test_login_inactive_user(self):
        with self.app.app_context():
            user = User(email='inactive@example.com', role='customer', isActive=False)
            user.set_password('pass1234')
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', data={
            'email': 'inactive@example.com',
            'password': 'pass1234'
        }, follow_redirects=True)

        if response.status_code == 200:
            print("Unactive account")
        else:
            print(f"Unexpected status code: {response.status_code}")

        assert b'account is not active' in response.data

    def test_login_invalid_password(self):
        with self.app.app_context():
            user = User(email='valid@example.com', isActive=True)
            user.set_password('correct_password')
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', data={
            'email': 'valid@example.com',
            'password': 'wrong_password'
        }, follow_redirects=True)

        if response.status_code == 200:
            print("Invalid password")
        else:
            print(f"Unexpected status code: {response.status_code}")
        assert b'Invalid password' in response.data

    def test_login_email_not_found(self):
        response = self.client.post('/login', data={
            'email': 'notfound@example.com',
            'password': 'any'
        }, follow_redirects=True)

        if response.status_code == 200:
            print("Email not found")
        else:
            print(f"Unexpected status code: {response.status_code}")
        assert b'Email not found' in response.data

    def test_logout(self):
        with self.app.app_context():
            user = User(email='logout@example.com', isActive=True)
            user.set_password('pass1234')
            db.session.add(user)
            db.session.commit()

        self.client.post('/login', data={'email': 'logout@example.com', 'password': 'pass1234'})
        response = self.client.get('/logout', follow_redirects=True)

        if response.status_code == 200:
            print("Account logged out and redirected to login page")
        else:
            print(f"Unexpected status code: {response.status_code}")


        html = response.data.decode('utf-8').lower()
        assert 'login' in html


