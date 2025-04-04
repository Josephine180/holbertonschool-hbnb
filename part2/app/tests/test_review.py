import unittest
from models.review import Review
from models.place import Place
from models.user import User
from persistence.repository import InMemoryRepository
import time


class TestReview(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test"""
        self.user_repository = InMemoryRepository()
        self.user = User(first_name="Alice", last_name="Doe",
                         email="alice@example.com")
        # Ajout de l'utilisateur dans le repository
        self.user_repository.add(self.user)

        self.place = Place(
            title="Beautiful House",
            description="A very nice place.",
            price=120,
            latitude=48.8566,
            longitude=2.3522,
            owner_id=self.user.id,
            user_repository=self.user_repository
        )

        self.review = Review(text="Amazing experience!",
                             rating=5, place=self.place, user=self.user)

    def test_review_creation(self):
        """Test que la review est bien créée avec les bonnes valeurs"""
        self.assertEqual(self.review.text, "Amazing experience!")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.place, self.place)
        self.assertEqual(self.review.user, self.user)

    def test_invalid_rating(self):
        """Test que la validation de la note fonctionne correctement"""
        with self.assertRaises(ValueError):
            Review(text="Too high rating", rating=6,
                   place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text="Too low rating", rating=0,
                   place=self.place, user=self.user)

    def test_empty_text(self):
        """Test que le texte de la review ne peut pas être vide"""
        with self.assertRaises(ValueError):
            Review(text="", rating=3, place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text="   ", rating=3, place=self.place, user=self.user)

    def test_invalid_place_or_user(self):
        """Test qu'une review sans place ou user valide lève une erreur"""
        with self.assertRaises(ValueError):
            Review(text="No place", rating=3, place=None, user=self.user)
        with self.assertRaises(ValueError):
            Review(text="No user", rating=3, place=self.place, user=None)
        with self.assertRaises(ValueError):
            Review(text="Invalid place", rating=3,
                   place="NotAPlace", user=self.user)
        with self.assertRaises(ValueError):
            Review(text="Invalid user", rating=3,
                   place=self.place, user="NotAUser")

    def test_update_review(self):
        """Test la mise à jour d'une review"""
        time.sleep(1)  # Pause pour observer le changement de timestamp
        old_updated_at = self.review.updated_at
        self.review.update_review("Updated review", 4)

        self.assertEqual(self.review.text, "Updated review")
        self.assertEqual(self.review.rating, 4)
        # Vérifie que updated_at a bien changé
        self.assertGreater(self.review.updated_at, old_updated_at)


if __name__ == '__main__':
    unittest.main()
