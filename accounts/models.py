from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    spouse = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    timezone = models.CharField(max_length=50, default="America/New_York")

    def __str__(self):
        return self.email or self.username
