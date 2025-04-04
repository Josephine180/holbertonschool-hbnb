from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from app.extensions import db, jwt, bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from app.extensions import db, jwt, bcrypt


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'your_secret_key'
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Créer les tables de la base de données
    with app.app_context():
        db.create_all()

    # Initialiser l'API
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1')

    # Initialiser l'admin dans un contexte d'application
    with app.app_context():
        from app.services import get_facade
        facade = get_facade()
        user_facade = facade.user_facade
        user_facade.initialize_admin()

    return app
