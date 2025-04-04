from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import get_facade

api = Namespace('reviews', description='Review operations')

# Définir le modèle de l'avis pour la validation des entrées
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        facade = get_facade()
        """Register a new review"""
        # Récupérer l'utilisateur actuel
        current_user_id = get_jwt_identity()

        # Récupérer les données envoyées
        review_data = api.payload
        # Assigner l'utilisateur authentifié
        review_data['user_id'] = current_user_id

        # Vérifier que le lieu existe
        place = facade.place_facade.get_place(
            review_data['place_id'], load_reviews=False)
        if not place:
            return {'message': 'Place not found'}, 400

        # Vérifier que l'utilisateur ne note pas son propre lieu
        if place.owner_id == current_user_id:  # Utiliser owner_id au lieu de owner.id
            return {'message': 'You cannot review your own place.'}, 400

        # Vérifier si l'utilisateur a déjà laissé un avis sur ce lieu
        existing_reviews = facade.review_facade.get_reviews_by_place(
            review_data['place_id'])
        if existing_reviews and any(review.user_id == current_user_id for review in existing_reviews):
            return {'message': 'You have already reviewed this place.'}, 400

        # Créer l'avis
        review = facade.review_facade.create_review(review_data)
        if review:
            return review.to_dict(), 201

        return {'message': 'Invalid data'}, 400

    def get(self):
        facade = get_facade()
        """Retrieve a list of all reviews"""
        reviews = facade.review_facade.get_all_reviews()
        # Sérialisation de tous les avis
        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        facade = get_facade()
        """Get review details by ID"""
        review = facade.review_facade.get_review(review_id)
        if review:
            return review.to_dict(), 200  # Sérialisation avant de renvoyer
        return {'message': 'Review not found'}, 404

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'You can only update your own review or be an admin')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        facade = get_facade()
        """Update a review's information"""
        user_id = get_jwt_identity()  # Récupère l'ID de l'utilisateur authentifié
        review = facade.review_facade.get_review(review_id)

        if not review:
            return {'message': 'Review not found'}, 404

        # Vérifie si l'utilisateur est le propriétaire ou un administrateur
        if review.user_id != user_id and not facade.user_facade.get_user(user_id).is_admin:
            return {'message': 'You can only update your own review or be an admin'}, 403

        review_data = api.payload
        new_text = review_data.get("text")
        new_rating = review_data.get("rating")

        if not new_text or len(new_text.strip()) == 0:
            return {'message': 'Review text cannot be empty'}, 400
        if not (1 <= new_rating <= 5):
            return {'message': 'Rating must be between 1 and 5'}, 400

        # Met à jour la review
        review.update_review(new_text, new_rating)
        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'You can only delete your own review or be an admin')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        facade = get_facade()
        """Delete a review"""
        user_id = get_jwt_identity()  # Récupère l'ID de l'utilisateur authentifié
        review = facade.review_facade.get_review(review_id)

        if not review:
            return {'message': 'Review not found'}, 404

        # Vérifie si l'utilisateur est le propriétaire ou un administrateur
        if review.user_id != user_id and not facade.user_facade.get_user(user_id).is_admin:
            return {'message': 'You can only delete your own review or be an admin'}, 403

        # Supprime la review
        facade.review_facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        facade = get_facade()
        """Get all reviews for a specific place"""
        # Utiliser la méthode directe pour éviter de vérifier l'existence de la place
        reviews = facade.review_facade.get_reviews_by_place_direct(place_id)
        if reviews is None:
            return {"message": "Place not found"}, 404

        if not reviews:  # Si la liste est vide, retourner une liste vide mais pas 404
            return [], 200

        # Sérialiser les avis avant de les retourner
        return [review.to_dict() for review in reviews], 200
