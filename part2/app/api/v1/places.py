from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Définir les modèles pour les entités associées
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Définir le modèle de place pour la validation des entrées et la documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.String, description="List of reviews on the place")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        owner_id = place_data.get('owner_id')

        # Vérifier si l'utilisateur existe
        owner = facade.get_user(owner_id)
        if not owner:
            return {"error": "Owner not found"}, 404

        # Appel à la méthode pour créer un lieu
        new_place = facade.create_place(place_data)

        # Utilisation de to_dict() pour retourner un dictionnaire de l'objet Place
        return new_place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()

        # Utilisation de to_dict() pour retourner chaque place sous forme de dictionnaire
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)

        if not updated_place:
            return {"error": "Place not found"}, 404

        return updated_place.to_dict(), 200


@api.route('/<place_id>/reviews')
class PlaceReviewResource(Resource):
    @api.expect(api.model('ReviewAssociation', {
        'review_id': fields.String(required=True, description="Review ID to associate with the place")
    }))
    @api.response(200, "Review successfully added to the place")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place or Review not found")
    def put(self, place_id):
        """Associer une review existante à un lieu"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        data = api.payload
        review = facade.get_review(data.get("review_id"))
        if not review:
            return {"error": "Review not found"}, 404

        # Ajout de la review
        try:
            place.add_review(review)
        except ValueError as e:
            return {"error": str(e)}, 400

        return place.to_dict(), 200
