# import unittest
# from datetime import date, timedelta
# from flask import url_for
# from flask_login import current_user
# from sqlalchemy.exc import IntegrityError
#
# from config import Config
# from greenlight import create_app
# from greenlight.models import User, Loan, UserLoan, db
#
#
# class TestAIRoutes(unittest.TestCase):
#     def setUp(self):
#         # Configure app
#         self.app = create_app(Config)
#         self.app.config.update({
#             'SERVER_NAME': 'localhost',
#             'WTF_CSRF_ENABLED': False,
#             'TESTING': True,
#             'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
#         })
#
#         # Create app context
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#
#         # Create test client
#         self.client = self.app.test_client()
#
#         # Create database
#         db.create_all()
#
#         # Create test user
#         self.test_user = User(
#             userId=1,
#             first_name="Test",
#             last_name="User",
#             email="test@example.com",
#             password="password"
#         )
#         db.session.add(self.test_user)
#         db.session.commit()
#
#         # Login user
#         with self.client.session_transaction() as sess:
#             sess['_user_id'] = str(self.test_user.userId)
#             sess['_fresh'] = True
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
#
#     def test_approval_form_post_success(self):
#         """Test successful loan application submission"""
#         form_data = {
#             'gender': 'Male',
#             'date_of_birth': (date.today() - timedelta(days=365 * 25)).strftime('%Y-%m-%d'),
#             'marital_status': 'Single',
#             'dependents': '0',
#             'education': 'Graduate',
#             'self_employment': 'No',
#             'applicant_income': '5000',
#             'coapplicant_income': '2000',
#             'loan_amount': '100000',
#             'loan_term': '360',
#             'credit_history': '1',
#             'property_area': 'Urban',
#             'submit': 'Submit'
#         }
#
#         # Verify initial state
#         self.assertEqual(Loan.query.count(), 0)
#         self.assertEqual(UserLoan.query.count(), 0)
#
#         # Submit form
#         response = self.client.post(
#             f'/approvalForm/{self.test_user.userId}',
#             data=form_data,
#             follow_redirects=True
#         )
#
#         # Verify response
#         self.assertEqual(response.status_code, 200)
#
#         # Verify database changes
#         loan = Loan.query.first()
#         self.assertIsNotNone(loan, "Loan should be created")
#
#         user_loan = UserLoan.query.first()
#         self.assertIsNotNone(user_loan, "UserLoan should be created")
#         self.assertEqual(user_loan.userId, self.test_user.userId)
#         self.assertEqual(user_loan.loanId, loan.loanId)
#
#     def test_approval_form_post_underage(self):
#         """Test underage loan application rejection"""
#         form_data = {
#             'gender': 'Male',
#             'date_of_birth': (date.today() - timedelta(days=365 * 17)).strftime('%Y-%m-%d'),
#             # ... other form fields same as above ...
#         }
#
#         response = self.client.post(
#             f'/approvalForm/{self.test_user.userId}',
#             data=form_data,
#             follow_redirects=True
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'at least 18 years old', response.data)
#         self.assertEqual(Loan.query.count(), 0, "No loan should be created")
#
#     def test_approved_route(self):
#         """Test approved loan page"""
#         with self.client:
#             response = self.client.get('/approved/75.5')
#             self.assertEqual(response.status_code, 200)
#             self.assertIn(b'Congratulations', response.data)
#             self.assertIn(b'75.5%', response.data)
#
#     def test_disapproved_route(self):
#         """Test disapproved loan page"""
#         with self.client:
#             response = self.client.get('/disapproved/30.2')
#             self.assertEqual(response.status_code, 200)
#             self.assertTrue(
#                 b'not approved' in response.data.lower() or
#                 b'not likely' in response.data.lower(),
#                 "Should show disapproval message"
#             )
#             self.assertIn(b'30.2%', response.data)
#
#
