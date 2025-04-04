from app.models.BaseModel import BaseModel
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, user_repository, amenity_repository, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = None
        self.reviews = []  # Liste pour stocker les avis associés
        self.amenities = amenities if amenities is not None else []

        # Vérification des contraintes de validation
        if not title or len(title) > 100:
            raise ValueError(
                "Le titre doit être compris entre 1 et 100 caractères")
        if price < 0:
            raise ValueError("Le prix doit être positif")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")

        # Vérification que l'utilisateur existe dans le repository
        owner = user_repository.get(owner_id)
        if owner is None:
            raise ValueError(
                "L'utilisateur spécifié comme propriétaire n'existe pas")
        self.owner = owner
        self.amenities = []
        if amenities:
            for amenity_id in amenities:
                amenity_obj = amenity_repository.get(amenity_id)
                if amenity_obj:
                    self.amenities.append(amenity_obj)
                else:
                    print(
                        f"Attention : L'amenity avec l'ID {amenity_id} n'existe pas !")

    def add_review(self, review):
        """Ajouter un avis à la place."""
        if hasattr(review, 'to_dict'):
            self.reviews.append(review)
        else:
            raise ValueError(
                "L'objet review doit posséder une méthode to_dict()")

    def add_amenity(self, amenity):
        """Ajouter un équipement à la place sans doublon."""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)
        elif not isinstance(amenity, Amenity):
            raise ValueError("L'objet amenity doit être de type Amenity")

    def to_dict(self):
        # Crée une liste d'objets amenity avec id et name si ce sont des objets Amenity
        amenities_data = [
            {"id": amenity.id, "name": amenity.name} if isinstance(amenity, Amenity)
            else None
            for amenity in self.amenities
        ]

        # Filtre les `None` pour ne pas avoir d'éléments vides
        amenities_data = [
            amenity for amenity in amenities_data if amenity is not None]

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": amenities_data
        }
