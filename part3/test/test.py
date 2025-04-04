import pytest
from flask_jwt_extended import create_access_token
from app import create_app
from app.services import facade

# Fixtures


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": False,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_user():
    return {
        'id': '1',
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password': 'adminpassword',
        'is_admin': True
    }


@pytest.fixture
def regular_user():
    return {
        'id': '2',
        'first_name': 'Regular',
        'last_name': 'User',
        'email': 'regular@example.com',
        'password': 'regularpassword',
        'is_admin': False
    }

# 1. Essayer de créer un utilisateur sans authentification


def test_create_user_without_authentication(client):
    user_data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'password': 'securepassword'
    }
    response = client.post('/api/v1/users/', json=user_data)
    assert response.status_code == 401

# 2. Essayer de créer un utilisateur avec un email déjà utilisé


def test_create_user_with_existing_email(client, admin_user, app):
    with app.app_context():
        access_token = create_access_token(
            identity=admin_user['id'], additional_claims={"is_admin": True})

    headers = {'Authorization': f'Bearer {access_token}'}
    user_data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'existing@example.com',
        'password': 'securepassword'
    }
    client.post('/api/v1/users/', json=user_data, headers=headers)
    response = client.post('/api/v1/users/', json=user_data, headers=headers)
    assert response.status_code == 400
    assert response.get_json().get('error') == 'Email already registered'

# 3. Un utilisateur non admin tente de créer un utilisateur


def test_create_user_as_non_admin(client, regular_user, app):
    with app.app_context():
        access_token = create_access_token(
            identity=regular_user['id'], additional_claims={"is_admin": False})

    headers = {'Authorization': f'Bearer {access_token}'}
    user_data = {
        'first_name': 'User',
        'last_name': 'Test',
        'email': 'usertest@example.com',
        'password': 'password123'
    }
    response = client.post('/api/v1/users/', json=user_data, headers=headers)
    assert response.status_code == 403

# 4. Un utilisateur modifie son propre profil


def test_update_own_profile(client, app):
    with app.app_context():
        user_data = {
            "first_name": "Regular",
            "last_name": "User",
            "email": "regular@example.com",
            "password": "password123"
        }
        regular_user = facade.create_user(user_data)  # Créer l'utilisateur
        access_token = create_access_token(
            identity=regular_user.id, additional_claims={"is_admin": False})

    headers = {'Authorization': f'Bearer {access_token}'}
    update_data = {'first_name': 'Updated', 'last_name': 'User'}
    response = client.put(
        f'/api/v1/users/{regular_user.id}', json=update_data, headers=headers)

    assert response.status_code == 200


# 5. Un utilisateur essaie de modifier son email ou mot de passe


def test_update_email_or_password(client, regular_user, app):
    with app.app_context():
        access_token = create_access_token(
            identity=regular_user['id'], additional_claims={"is_admin": False})

    headers = {'Authorization': f'Bearer {access_token}'}
    update_data = {'email': 'newemail@example.com', 'password': 'newpassword'}
    response = client.put(
        f'/api/v1/users/{regular_user["id"]}', json=update_data, headers=headers)
    assert response.status_code == 400
    assert response.get_json().get('error') == 'You cannot modify email or password'

# 6. Un admin modifie un utilisateur


def test_admin_updates_user(client, admin_user, regular_user, app):
    with app.app_context():
        access_token = create_access_token(
            identity=admin_user['id'], additional_claims={"is_admin": True})

    headers = {'Authorization': f'Bearer {access_token}'}
    update_data = {'first_name': 'Admin Updated'}
    response = client.put(
        f'/api/v1/users/{regular_user["id"]}', json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.get_json().get('first_name') == 'Admin Updated'


# 8. Essayer d'obtenir un utilisateur inexistant


def test_get_nonexistent_user(client, admin_user, app):
    with app.app_context():
        access_token = create_access_token(
            identity=admin_user['id'], additional_claims={"is_admin": True})

    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/api/v1/users/9999', headers=headers)
    assert response.status_code == 404
    assert response.get_json().get('error') == 'User not found'
