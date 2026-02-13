
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    organization = models.ForeignKey("core.Organization", on_delete=models.CASCADE, null=True)
    is_manager = models.BooleanField(default=False)

    is_observer = models.BooleanField(default=False)
    is_action_owner = models.BooleanField(default=False)
    is_safety_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



# class CustomUser(AbstractUser):
#     organization = models.ForeignKey(
#         'core.Organization',
#          on_delete=models.CASCADE,
#          blank=True,
#          null=True)
    # is_observer = models.BooleanField(default=False)
    # is_action_owner = models.BooleanField(default=False)
    # is_safety_manager = models.BooleanField(default=False)

#     @property
#     def is_manager(self):
#         return self.groups.filter(name='Managers').exists() or self.is_superuser

#     def __str__(self):
#         return self.get_full_name() or self.username

