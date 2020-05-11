from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = None
        if self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    def __str__(self):
        """Unicode representation of User."""
        return self.get_full_name()

    class Meta:
        """Meta definition for User."""

        ordering = ["-is_active"]
        verbose_name = "User"
        verbose_name_plural = "Users"
