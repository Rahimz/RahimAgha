from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # This field is required. Links Profile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any other fields you want for your user here
    bio = models.TextField(max_length=500, blank=True)
    ai_access = models.BooleanField(default=False)
    accounting_access = models.BooleanField(default=False)
    api_access = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username