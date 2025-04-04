from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from app.services import get_facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        facade = get_facade()
        """Register a new amenity (Admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'message': 'Admin privileges required'}, 403

        try:
            amenity_data = request.json

            # Vérification que le champ name est bien présent
            if 'name' not in amenity_data or not amenity_data['name'].strip():
                return {'message': "Le champ 'name' est requis et ne doit pas être vide."}, 400

            # Appel à la couche métier
            new_amenity = facade.amenity_facade.create_amenity(amenity_data)

            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'description': new_amenity.description
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        facade = get_facade()
        """Retrieve a list of all amenities"""
        amenities = facade.amenity_facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        facade = get_facade()
        """Get amenity details by ID"""
        amenity = facade.amenity_facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404

        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        facade = get_facade()
        """Update an amenity's information (Admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'message': 'Admin privileges required'}, 403

        try:
            amenity_data = request.json

            # Vérification que le champ name est bien présent
            if 'name' not in amenity_data or not amenity_data['name'].strip():
                return {'message': "Le champ 'name' est requis et ne doit pas être vide."}, 400

            updated_amenity = facade.amenity_facade.update_amenity(
                amenity_id, amenity_data)
            if not updated_amenity:
                return {'message': 'Amenity not found'}, 404

            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400


@api.route('/<amenity_id>/places')
class AmenityPlaces(Resource):
    @api.response(200, 'List of places with this amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        facade = get_facade()
        """Get all places that have this specific amenity"""
        # Vérifier d'abord si l'équipement existe
        amenity = facade.amenity_facade.get_amenity(amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404

        # Récupérer les lieux qui ont cet équipement grâce à la relation
        places = facade.amenity_facade.get_places_with_amenity(amenity_id)

        # Sérialiser les lieux avant de les retourner
        return [place.to_dict() for place in places], 200
