import unittest
from flask import Flask
from app.api.v1.users import api as users_ns
from app.services.facade import HBnBFacade
from flask_restx import Api


class UserTestCase(unittest.TestCase):
    def setUp(self):
        """Configure the test client and database"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(users_ns, path='/api/v1/users')
        self.client = self.app.test_client()

        # Reset the facade (in-memory repository)
        self.facade = HBnBFacade()

    def test_create_user(self):
        """Test user creation"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_user_duplicate_email(self):
        """Test that duplicate emails are not allowed"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com"
        }
        # Create the first user
        self.client.post('/api/v1/users/', json=user_data)

        # Try to create a user with the same email
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email already registered")

    def test_get_user(self):
        """Test retrieving a user by ID"""
        user_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        }
        create_response = self.client.post('/api/v1/users/', json=user_data)
        user_id = create_response.json["id"]

        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["email"], "alice@example.com")

    def test_get_nonexistent_user(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/invalid_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "User not found")


if __name__ == '__main__':
    unittest.main()
