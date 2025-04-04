from app.models.BaseModel import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, name: str, description: str = ""):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Le nom de l'amenity ne doit pas être vide.")
        if len(name) > 50:
            raise ValueError(
                "Le nom de l'amenity ne doit pas dépasser 50 caractères.")

        # Validation de la description
        if not isinstance(description, str):
            raise ValueError(
                "La description doit être une chaîne de caractères.")
        if len(description) > 255:
            raise ValueError(
                "La description ne doit pas dépasser 255 caractères.")

        self.name = name
        self.description = description

    def to_dict(self):
        """Retourne une représentation sous forme de dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "places_count": self.places.count() if hasattr(self, 'places') else 0
        }
