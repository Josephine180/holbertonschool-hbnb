from app.services.repositories.place_repository import PlaceRepository
from app.models.place import Place


class PlaceFacade:
    def __init__(self, user_facade, amenity_facade):
        self.place_repo = PlaceRepository()
        self.user_facade = user_facade
        self.amenity_facade = amenity_facade

    def create_place(self, place_data):
        """Crée un lieu et retourne l'objet du lieu créé"""
        owner_id = place_data.get('owner_id')
        amenities_ids = place_data.get('amenities', [])

        # Vérifier si l'utilisateur existe
        owner = self.user_facade.get_user(owner_id)
        if not owner:
            return {"error": "Owner not found"}, 404

        # Supprimer les reviews s'ils existent dans les données (on ne les gère pas ici)
        place_data.pop("reviews", None)

        # Créer un objet Place
        new_place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=owner_id
        )

        # Ajouter les amenities
        for amenity_id in amenities_ids:
            amenity = self.amenity_facade.get_amenity(amenity_id)
            if amenity:
                new_place.add_amenity(amenity)

        # Enregistrer le lieu
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id, load_reviews=True):
        """
        Récupère un lieu par son ID

        Args:
            place_id: ID du lieu à récupérer
            load_reviews: Si True, charge les reviews associées (défaut=True)
        """
        place = self.place_repo.get(place_id)
        # Avec les relations SQLAlchemy, nous n'avons plus besoin de charger manuellement
        # les reviews et amenities, ils seront chargés automatiquement lors de l'accès
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        return places

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id, load_reviews=False)
        if not place:
            return {"error": "Place not found"}, 404

        # Vérifier le prix uniquement s'il est fourni
        if 'price' in place_data and place_data.get('price', 0) <= 0:
            return {"error": "Le prix doit être positif"}, 400

        # Mettre à jour les attributs de base
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']

        # Gestion des amenities si présentes
        if 'amenities' in place_data:
            # Réinitialiser les amenities
            place.amenities = []

            for amenity_id in place_data['amenities']:
                amenity = self.amenity_facade.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        # Sauvegarder les modifications
        place.save()
        return place

    def delete_place(self, place_id):
        place = self.get_place(place_id, load_reviews=False)
        if not place:
            return {"error": "Place not found"}, 404
        self.place_repo.delete(place_id)
        return {"message": "Place successfully deleted"}, 200

    def get_places_by_user(self, user_id):
        """Récupère tous les lieux appartenant à un utilisateur donné"""
        user = self.user_facade.get_user(user_id)
        if not user:
            return None
        return user.places.all()
