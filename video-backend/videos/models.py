from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None  # Remove the username field if not needed

    def __str__(self):
        return self.email
#    email = models.EmailField(unique=True)

#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = []
 #   REQUIRED_FIELDS = ['username']

#    def __str__(self):
#        return self.username
    