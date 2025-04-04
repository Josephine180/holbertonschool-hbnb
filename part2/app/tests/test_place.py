import unittest
from models.user import User
from models.place import Place
from persistence.repository import InMemoryRepository


class TestPlace(unittest.TestCase):

    def setUp(self):
        """Méthode exécutée avant chaque test pour initialiser les données"""
        self.user_repo = InMemoryRepository()
        self.owner = User(first_name="Alice", last_name="Smith",
                          email="alice@example.com")
        self.user_repo.add(self.owner)  # Ajoute l'utilisateur au repository

    def test_place_creation_success(self):
        """Test de création d'un lieu avec des données valides"""
        place = Place(
            title="Bel Appartement",
            description="Vue sur mer",
            price=120,
            latitude=48.8566,
            longitude=2.3522,
            owner_id=self.owner.id,
            user_repository=self.user_repo
        )
        self.assertEqual(place.title, "Bel Appartement")
        self.assertEqual(place.price, 120)
        self.assertEqual(place.owner, self.owner)
        print("✅ Test de création réussi")

    def test_place_creation_invalid_price(self):
        """Test d'erreur lors d'une création avec un prix négatif"""
        with self.assertRaises(ValueError) as context:
            Place("Petit studio", "Proche métro", -50,
                  48.85, 2.34, self.owner.id, self.user_repo)
        self.assertEqual(str(context.exception), "Le prix doit être positif")

    def test_place_creation_invalid_latitude(self):
        """Test d'erreur avec une latitude invalide"""
        with self.assertRaises(ValueError):
            Place("Loft", "Très grand", 300, 95,
                  2.34, self.owner.id, self.user_repo)

    def test_place_creation_invalid_owner(self):
        """Test d'erreur lorsqu'un propriétaire n'existe pas"""
        with self.assertRaises(ValueError):
            Place("Maison", "Jardin", 200, 48.85, 2.34,
                  "inexistant_id", self.user_repo)


if __name__ == "__main__":
    unittest.main()
