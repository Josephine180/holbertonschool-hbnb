from app.models.BaseModel import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.validate()  # Appel à la méthode de validation

    def validate(self):
        """Valide les données de la review"""
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Review text cannot be empty")

        if not isinstance(self.place, Place):
            raise ValueError("Place must be a valid Place instance")
        if not isinstance(self.user, User):
            raise ValueError("User must be a valid User instance")

    def to_dict(self):
        """Retourne une représentation sous forme de dictionnaire"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id,  # Utiliser l'ID de l'utilisateur
            "place_id": self.place.id  # Utiliser l'ID du lieu
        }

    def update_review(self, new_text, new_rating):
        """Met à jour la review et sauvegarde les modifications"""
        self.text = new_text
        self.rating = new_rating
        self.validate()  # Revalidation après modification
        self.save()  # Sauvegarde les modifications (avec mise à jour de `updated_at`)
