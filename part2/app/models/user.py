#!/usr/bin/python3
import re
from app.models.BaseModel import BaseModel


class User(BaseModel):

    existing_emails = []

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate_email(email)
        self.validate_name(first_name, last_name)
        self.check_email_uniqueness(email)
        User.existing_emails.append(email)

    def validate_email(self, email):
        email_regex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if not re.match(email_regex, email):
            raise ValueError("Email invalide")

    def validate_name(self, first_name, last_name):
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError(
                "Le nom ou prénom ne doit pas dépasser 50 caractères.")

    def check_email_uniqueness(self, email):
        if email in User.existing_emails:
            raise ValueError(f"L'email {email} est déjà utilisé.")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
