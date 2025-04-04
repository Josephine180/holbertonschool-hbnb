from app.extensions import db, bcrypt
from app.models.BaseModel import BaseModel
import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relations
    places = db.relationship('Place', backref='owner',
                             lazy='dynamic', cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='user',
                              lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate_email(email)
        self.validate_name(first_name, last_name)

        if password:
            self.hash_password(password)  # Hash the password if provided

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def validate_email(self, email):
        email_regex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if not re.match(email_regex, email):
            raise ValueError("Email invalide")

    def validate_name(self, first_name, last_name):
        if not first_name or not last_name:
            raise ValueError("Le nom et le prénom ne doivent pas être vides.")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError(
                "Le nom ou prénom ne doit pas dépasser 50 caractères.")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
