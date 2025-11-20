from django.db import models

# Create your models here.

# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_observer = models.BooleanField(default=True)
    is_action_owner = models.BooleanField(default=False)
    is_safety_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username

