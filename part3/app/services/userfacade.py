
from app.services.repositories.user_repository import UserRepository
from app.models.user import User


class UserFacade:
    def __init__(self):
        self.user_repo = UserRepository()

    def initialize_admin(self):
        admin_email = "admin@example.com"
        if self.get_user_by_email(admin_email):
            return

        admin_user = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            password="adminpassword",
            is_admin=True
        )
        self.user_repo.add(admin_user)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Traiter séparément le mot de passe s'il est fourni
        if 'password' in user_data:
            password = user_data.pop('password')
            if password:
                user.hash_password(password)

        # Mettre à jour les autres attributs
        if user_data:
            self.user_repo.update(user_id, user_data)

        return user

    def get_user_places(self, user_id):
        """Récupère tous les lieux appartenant à un utilisateur donné"""
        user = self.get_user(user_id)
        if not user:
            return None
        return user.places.all()

    def get_user_reviews(self, user_id):
        """Récupère tous les avis écrits par un utilisateur donné"""
        user = self.get_user(user_id)
        if not user:
            return None
        return user.reviews.all()
