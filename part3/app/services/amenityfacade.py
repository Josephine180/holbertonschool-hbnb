from app.services.repositories.amenity_repository import AmenityRepository
from app.models.amenity import Amenity


class AmenityFacade:
    def __init__(self):
        self.amenity_repo = AmenityRepository()

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data:
            raise ValueError("Missing 'name' field")

        # Extraire les données nécessaires pour l'Amenity
        name = amenity_data.get('name')
        description = amenity_data.get('description', '')

        # Créer l'objet Amenity
        amenity = Amenity(name=name, description=description)

        # Ajouter à la base de données
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all() or []

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        # Mettre à jour les attributs de l'amenity
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        if 'description' in amenity_data:
            amenity.description = amenity_data.get('description', '')

        # Sauvegarder les modifications
        amenity.save()
        return amenity

    def get_places_with_amenity(self, amenity_id):
        """
        Récupère tous les lieux qui disposent d'un équipement spécifique
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        return amenity.places.all()
