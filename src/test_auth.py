import unittest
from app import app
from flask_jwt_extended import create_access_token
from models import User, db

class TestRBAC(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Create a test user
        self.test_user = User(email="testuser@example.com")
        self.test_user.set_password("password")
        self.test_user.is_admin = False
        db.session.add(self.test_user)
        db.session.commit()
        
        # Create an admin user
        self.test_admin = User(email="admin@example.com")
        self.test_admin.set_password("adminpassword")
        self.test_admin.is_admin = True
        db.session.add(self.test_admin)
        db.session.commit()

    def test_normal_user_access(self):
        # Login as normal user
        access_token = create_access_token(identity=self.test_user.id, additional_claims={"is_admin": False})
        
        # Test protected endpoint for normal user
        response = self.app.get('/admin/data', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_admin_user_access(self):
        # Login as admin user
        access_token = create_access_token(identity=self.test_admin.id, additional_claims={"is_admin": True})
        
        # Test protected endpoint for admin user
        response = self.app.get('/admin/data', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)  # Success

if __name__ == '__main__':
    unittest.main()

