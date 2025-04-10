from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # Pour que SQLAlchemy ne crée pas de table pour cette classe

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Sauvegarde l'instance dans la base de données."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprime l'instance de la base de données."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Sauvegarde et met à jour updated_at