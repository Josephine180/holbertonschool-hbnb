#!/usr/bin/env python3
import uuid
import bcrypt

# Fonction pour générer un UUID


def generate_uuid():
    return str(uuid.uuid4())

# Fonction pour hasher un mot de passe avec bcrypt


def hash_password(password):
    # Encode la chaîne en bytes
    password_bytes = password.encode('utf-8')
    # Génère un sel et hash le mot de passe
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
    # Retourne le hash en format string
    return hashed.decode('utf-8')


# Exemple d'utilisation pour générer des UUIDs
print("Génération d'UUIDs pour les données initiales:")
print(f"UUID pour administrateur: {generate_uuid()}")
print(f"UUID pour WiFi: {generate_uuid()}")
print(f"UUID pour Swimming Pool: {generate_uuid()}")
print(f"UUID pour Air Conditioning: {generate_uuid()}")

# Génération du hash pour le mot de passe admin
admin_password = "admin1234"
hashed_password = hash_password(admin_password)
print(f"\nMot de passe admin hashé: {hashed_password}")

# Génère des instructions SQL pour insérer des données avec des UUIDs
print("\nInstructions SQL pour insérer l'administrateur:")
admin_uuid = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"
print(f"""
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '{admin_uuid}',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '{hashed_password}',
    TRUE
);
""")

# Génère des instructions SQL pour insérer les équipements
amenities = ["WiFi", "Swimming Pool", "Air Conditioning"]
print("Instructions SQL pour insérer les équipements:")
print("INSERT INTO amenities (id, name) VALUES")
amenity_values = []
for amenity in amenities:
    amenity_values.append(f"    ('{generate_uuid()}', '{amenity}')")
print(",\n".join(amenity_values) + ";")
