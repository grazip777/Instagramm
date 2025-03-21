from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# User Manager
class UserManager(BaseUserManager):
    def _create_user(self, email, password, username=None, **extra_fields):
        # Если email не был передан, выбрасываем исключение
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        # Создаем пользователя с email и username
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

# Model User
class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='users_avatars/',
                               default='users_avatars/default_avatar/default_avatar.jpeg')
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []