import os
from pathlib import Path

# Chemin absolu du dossier instance
INSTANCE_DIR = Path(__file__).resolve().parent / "instance"

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    # Chemin explicite vers la base de données existante
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{INSTANCE_DIR / "development.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False