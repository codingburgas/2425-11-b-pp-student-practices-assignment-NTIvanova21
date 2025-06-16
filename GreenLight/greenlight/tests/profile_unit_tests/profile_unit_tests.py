import unittest

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

from greenlight import create_app, db
from greenlight.models import User

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@localhost/TestDatabase?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'

class ProfileRoutesTestCase(unittest.TestCase):
    """Unit tests for the profile-related routes."""

    def setUp(self):
        """Set up test client, app context, and test user."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create test user and log in
        self.test_user = User(
            userId=1,
            first_name='Test',
            middle_name='Middle',
            last_name='User',
            email='test@example.com',
            password=generate_password_hash('old_password'),
            role='admin',
            profilePicture='default.jpg',
            isActive=True
        )
        db.session.add(self.test_user)
        db.session.commit()

        with self.client:
            response = self.client.post('/login', data={
                'email': 'test@example.com',
                'password': 'old_password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Clean up database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_profile_page(self):
        """Test that the profile page displays correctly."""
        with self.app.test_request_context():
            url = url_for('profile.profile', userId=1)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Test User', response.data)

    def test_profile_page_unauthorized_access(self):
        """Test that accessing another user's profile is forbidden."""

        # Create another user
        another_user = User(
            userId=2,
            first_name='Another',
            middle_name="Middle",
            last_name='User',
            email='another@example.com',
            password=generate_password_hash('password'),
            role='admin',
            profilePicture='default.jpg',
            isActive=True
        )
        db.session.add(another_user)
        db.session.commit()


        response = self.client.get(url_for('profile.profile', userId=2))
        self.assertEqual(response.status_code, 403)

    def test_change_profile_picture(self):
        """Test successfully changing the profile picture."""

        response = self.client.get(
            url_for('profile.change_profile_picture',
                   userId=1,
                   profilePicture='new_picture.jpg'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        updated_user = User.query.get(1)
        self.assertEqual(updated_user.profilePicture, 'new_picture.jpg')

    def test_change_profile_picture_unauthorized(self):
        """Test that users cannot change another user's profile picture."""
        another_user = User(
            userId=2,
            email='another@example.com',
            password=generate_password_hash('password'),
            profilePicture='default.jpg',
            isActive=True
        )
        db.session.add(another_user)
        db.session.commit()


        response = self.client.get(
            url_for('profile.change_profile_picture',
                    userId=2,
                    profilePicture='new_picture.jpg'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 403)

    def test_change_password_success(self):
        """Test successful password change."""
        response = self.client.post(
            url_for('profile.change_password', userId=1),
            data={
                'current_password': 'old_password',
                'new_password': 'new_password',
                'confirm_password': 'new_password'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        updated_user = User.query.get(1)
        self.assertTrue(check_password_hash(updated_user.password, 'new_password'))
        self.assertIn(b'Password was successfully changed!', response.data)

    def test_change_password_wrong_current_password(self):
        """Test password change fails when current password is incorrect."""
        response = self.client.post(
            url_for('profile.change_password', userId=1),
            data={
                'current_password': 'wrong_password',
                'new_password': 'new_password',
                'confirm_password': 'new_password'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Current password is incorrect.', response.data)

    def test_change_password_mismatch_new_passwords(self):
        """Test password change fails when new passwords do not match."""
        response = self.client.post(
            url_for('profile.change_password', userId=1),
            data={
                'current_password': 'old_password',
                'new_password': 'new_password',
                'confirm_password': 'different_password'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New passwords do not match.', response.data)

    def test_change_password_unauthorized(self):
        """Test that a user cannot change another user's password."""
        another_user = User(
            userId=2,
            email='another@example.com',
            password=generate_password_hash('password'),
            profilePicture='default.jpg',
            isActive=True
        )
        db.session.add(another_user)
        db.session.commit()

        response = self.client.post(
            url_for('profile.change_password', userId=2),
            data={
                'current_password': 'password',
                'new_password': 'new_password',
                'confirm_password': 'new_password'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 403)