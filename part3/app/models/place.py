from app.models.BaseModel import BaseModel
from app.extensions import db
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)

    # Relations
    reviews = db.relationship(
        'Review', backref='place', lazy='dynamic', cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='dynamic', backref=db.backref('places', lazy='dynamic'))

    def __init__(self, title, description, price, latitude, longitude, owner_id, user_repository=None, amenity_repository=None, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

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

    def add_review(self, review):
        """Ajouter un avis à la place."""
        if hasattr(review, 'to_dict'):
            self.reviews.append(review)
        else:
            raise ValueError(
                "L'objet review doit posséder une méthode to_dict()")

    def add_amenity(self, amenity):
        """Ajouter un équipement à la place sans doublon."""
        if hasattr(amenity, 'id') and amenity not in self.amenities:
            self.amenities.append(amenity)
        elif not hasattr(amenity, 'id'):
            raise ValueError("L'objet amenity doit avoir un attribut 'id'")

    def to_dict(self):
        # Sérialiser les amenities
        amenities_data = [
            {"id": amenity.id, "name": amenity.name}
            for amenity in self.amenities
        ]

        # Sérialiser les reviews
        reviews_data = [review.to_dict() for review in self.reviews]

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "reviews": reviews_data,
            "amenities": amenities_data
        }
