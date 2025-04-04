from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import get_facade
from app.models.user import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    def post(self):
        facade = get_facade()
        """Register a new user (Admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Forbidden'}, 403

        user_data = api.payload

        if not user_data['first_name'].strip() or not user_data['last_name'].strip():
            return {'error': 'First name and last name cannot be empty'}, 400
        if not user_data['password'].strip():
            return {'error': 'Password cannot be empty'}, 400

        try:
            User.validate_email(None, user_data['email'])
        except ValueError as e:
            return {'error': str(e)}, 400

        existing_user = facade.user_facade.get_user_by_email(
            user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.user_facade.create_user(user_data)
        return {'id': new_user.id, 'message': 'User successfully created'}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        facade = get_facade()
        """Get the list of users"""
        users = facade.user_facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        facade = get_facade()
        user = facade.user_facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model, validate=False)
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid modification')
    def put(self, user_id):
        facade = get_facade()
        """Update user details (Self or Admin)"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        # Seuls les admins peuvent modifier un autre utilisateur
        if current_user != str(user_id) and not is_admin:
            return {'message': 'Unauthorized action'}, 403

        user_data = api.payload
        update_fields = {}

        # Tout le monde peut modifier prénom/nom
        if 'first_name' in user_data and user_data['first_name'].strip():
            update_fields['first_name'] = user_data['first_name'].strip()
        if 'last_name' in user_data and user_data['last_name'].strip():
            update_fields['last_name'] = user_data['last_name'].strip()

        # Un utilisateur normal ne peut pas modifier email ou mot de passe
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        # Si admin, il peut tout modifier
        if is_admin:
            if 'email' in user_data:
                try:
                    User.validate_email(None, user_data['email'])
                    update_fields['email'] = user_data['email']
                except ValueError as e:
                    return {'error': str(e)}, 400

            if 'password' in user_data and user_data['password'].strip():
                update_fields['password'] = user_data['password'].strip()

        user = facade.user_facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.user_facade.update_user(user_id, update_fields)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200


@api.route('/<user_id>/places')
class UserPlaces(Resource):
    @api.response(200, 'List of places owned by the user retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        facade = get_facade()
        """Get all places owned by a specific user"""
        # Vérifier d'abord si l'utilisateur existe
        user = facade.user_facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        # Récupérer les places de l'utilisateur grâce à la relation
        places = facade.place_facade.get_places_by_user(user_id)

        # Sérialiser les places avant de les retourner
        return [place.to_dict() for place in places], 200


@api.route('/<user_id>/reviews')
class UserReviews(Resource):
    @api.response(200, 'List of reviews written by the user retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        facade = get_facade()
        """Get all reviews written by a specific user"""
        # Vérifier d'abord si l'utilisateur existe
        user = facade.user_facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        # Récupérer les reviews de l'utilisateur grâce à la relation
        reviews = facade.review_facade.get_reviews_by_user(user_id)

        # Sérialiser les reviews avant de les retourner
        return [review.to_dict() for review in reviews], 200
