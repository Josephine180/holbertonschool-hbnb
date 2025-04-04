from app.models.BaseModel import BaseModel
from app.extensions import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey(
        'places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating

        # Si place et user sont des instances complètes, nous récupérons leur ID
        if hasattr(place, 'id'):
            self.place_id = place.id
            self.place = place
        else:
            self.place_id = place

        if hasattr(user, 'id'):
            self.user_id = user.id
            self.user = user
        else:
            self.user_id = user

        self.validate()  # Appel à la méthode de validation

    def validate(self):
        """Valide les données de la review"""
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Review text cannot be empty")

    def to_dict(self):
        """Retourne une représentation sous forme de dictionnaire"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def update_review(self, new_text, new_rating):
        """Met à jour la review et sauvegarde les modifications"""
        self.text = new_text
        self.rating = new_rating
        self.validate()  # Revalidation après modification
        self.save()  # Sauvegarde les modifications (avec mise à jour de `updated_at`)
