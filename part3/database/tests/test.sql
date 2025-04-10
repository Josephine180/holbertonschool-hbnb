-- Test de sélection des données
-- Vérifier l'administrateur
SELECT * FROM users WHERE is_admin = TRUE;

-- Vérifier les équipements 
SELECT * FROM amenities;

-- Exemple d'insertion d'un utilisateur normal
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password
) VALUES (
    '7ba7b810-9dad-11d1-80b4-00c04fd430c8',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2a$12$a1B2c3D4e5F6g7H8i9J0k.LmNoPqRsTuVwX.YzAbC.DeF.GhIjK1L'
);

-- Exemple d'insertion d'un lieu
INSERT INTO places (
    id,
    title,
    description,
    price,
    latitude,
    longitude,
    owner_id
) VALUES (
    '8ba7b810-9dad-11d1-80b4-00c04fd430c8',
    'Bel appartement au centre-ville',
    'Magnifique appartement de 2 chambres avec vue sur la ville',
    120.00,
    48.8566,
    2.3522,
    '7ba7b810-9dad-11d1-80b4-00c04fd430c8'
);

-- Exemple d'association d'équipements à un lieu
INSERT INTO place_amenity (
    place_id,
    amenity_id
) VALUES 
    ('8ba7b810-9dad-11d1-80b4-00c04fd430c8', '550e8400-e29b-41d4-a716-446655440000'),
    ('8ba7b810-9dad-11d1-80b4-00c04fd430c8', '6ba7b811-9dad-11d1-80b4-00c04fd430c8');

-- Exemple d'insertion d'un avis
INSERT INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id
) VALUES (
    '9ba7b810-9dad-11d1-80b4-00c04fd430c8',
    'Très bel appartement, propre et bien situé',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    '8ba7b810-9dad-11d1-80b4-00c04fd430c8'
);

-- Exemple de requête pour obtenir tous les lieux avec leurs équipements
SELECT p.id, p.title, a.name AS amenity_name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
ORDER BY p.title;

-- Exemple de requête pour obtenir la moyenne des notes pour un lieu
SELECT p.id, p.title, AVG(r.rating) AS average_rating
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title;

-- Exemple de requête pour obtenir les lieux d'un utilisateur
SELECT p.id, p.title, p.price 
FROM places p
WHERE p.owner_id = '7ba7b810-9dad-11d1-80b4-00c04fd430c8';

-- Exemple de mise à jour d'un lieu
UPDATE places 
SET price = 150.00, description = 'Appartement rénové au centre-ville avec vue panoramique'
WHERE id = '8ba7b810-9dad-11d1-80b4-00c04fd430c8';

-- Exemple de suppression d'un avis
DELETE FROM reviews 
WHERE id = '9ba7b810-9dad-11d1-80b4-00c04fd430c8';

-- Test de la contrainte d'unicité (un utilisateur ne peut pas laisser deux avis sur le même lieu)
-- Cette insertion devrait échouer si l'avis existe déjà
INSERT INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id
) VALUES (
    'aba7b810-9dad-11d1-80b4-00c04fd430c8',
    'Un deuxième avis qui devrait être rejeté',
    4,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    '8ba7b810-9dad-11d1-80b4-00c04fd430c8'
);