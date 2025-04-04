import unittest
from flask import Flask
from api.v1.amenities import api as amenities_ns
from services.facade import HBnBFacade
from flask_restx import Api


class AmenityTestCase(unittest.TestCase):
    def setUp(self):
        """Configuration du client de test et de la base in-memory"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(amenities_ns, path='/api/v1/amenities')
        self.client = self.app.test_client()

        # Reset de la façade (repository en mémoire)
        self.facade = HBnBFacade()

    def test_create_amenity(self):
        """Test de la création d'un amenity"""
        amenity_data = {"name": "Piscine"}
        response = self.client.post('/api/v1/amenities/', json=amenity_data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_amenity_without_name(self):
        """Test de création d'un amenity sans nom (doit échouer)"""
        amenity_data = {"name": ""}
        response = self.client.post('/api/v1/amenities/', json=amenity_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Le champ 'name' est requis et ne doit pas être vide.")


    def test_get_amenity(self):
        """Test de récupération d'un amenity par ID"""
        amenity_data = {"name": "WiFi"}
        create_response = self.client.post('/api/v1/amenities/', json=amenity_data)
        amenity_id = create_response.json["id"]

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "WiFi")

    def test_get_nonexistent_amenity(self):
        """Test de récupération d'un amenity inexistant"""
        response = self.client.get('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Amenity not found")


if __name__ == '__main__':
    unittest.main()

