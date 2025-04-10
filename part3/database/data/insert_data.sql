-- SQLite compatible data insertion
-- Insertion de l'administrateur
INSERT OR IGNORE INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    -- Hash du mot de passe 'admin1234' généré avec bcrypt2
    '$2a$12$RWH8y0WgWnrC7YrPQvVJ1eDgx0hcGNHJHFeq1gTK17IFGlWLcXsT6',
    1  -- 1 pour true dans SQLite
);

-- Insertion des équipements initiaux
INSERT OR IGNORE INTO amenities (
    id,
    name,
    description
) VALUES 
    ('550e8400-e29b-41d4-a716-446655440000', 'WiFi', 'Connexion internet sans fil'),
    ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'Swimming Pool', 'Piscine privée ou commune'),
    ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'Air Conditioning', 'Climatisation dans toutes les pièces');