from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.db.models import UniqueConstraint

# User Manager
class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
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


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users_avatars/', default='users_avatars/default.png')
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    followers_count = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def follow(self, user):
        if self != user:
            subscription, created = Subscription.objects.get_or_create(follower=self, following=user)
            if created:
                user.followers_count += 1
                user.save()

    def unfollow(self, user):
        deleted, _ = Subscription.objects.filter(follower=self, following=user).delete()
        if deleted > 0:
            # Пересчитываем реальные подписчики
            user.followers_count = Subscription.objects.filter(following=user).count()
            user.save()

    def is_following(self, user):
        return Subscription.objects.filter(follower=self, following=user).exists()

    def is_followed_by(self, user):
        return Subscription.objects.filter(follower=user, following=self).exists()


class Subscription(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(default=now)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['follower', 'following'], name='unique_subscription')
        ]
        ordering = ['-subscribed_at']

