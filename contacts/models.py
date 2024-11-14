from django.db import models


class Contact(models.Model):
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    phone = models.CharField(
        max_length=14,
        null=True,
        blank=True
    )
    email = models.EmailField(
        null=True, 
        blank=True
    )
    require = models.CharField(
        max_length=14,
        default='message'
    )
    created = models.DateField(
        auto_now_add=True
    )
    is_checked = models.BooleanField(
        default=False
    )
    is_spam = models.BooleanField(
        default=False
    )
