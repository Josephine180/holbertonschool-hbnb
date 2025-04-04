from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app.services import get_facade

api = Namespace('auth', description='Authentication operations')

# Modèle pour la validation de l'entrée
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        facade = get_facade()
        """Authentifier l'utilisateur et retourner un token JWT"""
        credentials = api.payload  # Récupérer l'email et le mot de passe du payload

        # Étape 1 : Récupérer l'utilisateur en fonction de l'email
        user = facade.user_facade.get_user_by_email(credentials['email'])

        # Étape 2 : Vérifier si l'utilisateur existe et si le mot de passe est correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Identifiants invalides'}, 401

        # Étape 3 : Créer un token JWT avec l'ID de l'utilisateur et le flag is_admin
        access_token = create_access_token(identity=str(
            user.id), additional_claims={"is_admin": user.is_admin})

        # Étape 4 : Retourner le token JWT au client
        return {'access_token': access_token}, 200
