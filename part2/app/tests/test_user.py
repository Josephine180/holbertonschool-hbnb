import unittest
from models.user import User


class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)  # Default value

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="Doe", email="invalide-email")

    def test_name_length(self):
        with self.assertRaises(ValueError):
            User(first_name="A" * 51, last_name="Doe",
                 email="john.doe@example.com")


if __name__ == "__main__":
    unittest.main()
