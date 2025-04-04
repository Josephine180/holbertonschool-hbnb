from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('protected', description='Secured Endpoints')


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Un endpoint protégé qui nécessite un token JWT valide"""
        current_user_id = get_jwt_identity()  # Retourne juste l'ID (string)
        # Récupère is_admin depuis additional_claims
        is_admin = get_jwt()["is_admin"]

        return {'message': f'Hello, user {current_user_id}'}, 200
