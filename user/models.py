from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


# User Manager
class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and authentication.

    This manager provides methods to create regular users and superusers
    with email-based authentication. The `_create_user` method serves as the
    base for creating users with default attributes and validations.

    Methods:
        - _create_user(email, password, **extra_fields): 
          Private method to create a user with specified email and password.
        - create_user(email, password, **extra_fields): 
          Public method to create a standard user with default non-staff status.
        - create_superuser(email, password, **extra_fields): 
          Public method to create a superuser with admin privileges.
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.

        Args:
            email (str): Email address of the user.
            password (str): User's password.
            **extra_fields: Additional optional parameters for the user.

        Returns:
            User: New user object with is_staff=False and is_active=True.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.

        Args:
            email (str): Email address of the superuser.
            password (str): Superuser's password.
            **extra_fields: Additional optional parameters (e.g., is_staff=True).

        Raises:
            ValueError: If is_staff or is_superuser is not explicitly set to True.

        Returns:
            User: New superuser object with admin privileges.
        """
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
    """
    Represents a user in the system, inheriting from Django's AbstractUser.
    This model overrides the default fields for more specific use cases, 
    including unique email-based authentication and support for avatars.
    """

    email = models.EmailField(unique=True)  # User's email address, serves as the unique identifier
    avatar = models.ImageField(upload_to='users_avatars/')  # Profile picture of the user
    username = models.CharField(max_length=50)  # User's display name
    is_active = models.BooleanField(default=True)  # Indicates if the user's account is active

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def follow(self, user):
        """Subscribe to another user"""
        if self != user:
            Subscription.objects.get_or_create(follower=self, following=user)

    def unfollow(self, user):
        """Unsubscribe from the user"""
        Subscription.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        """Check if the current user is signed for another"""
        return Subscription.objects.filter(follower=self, following=user).exists()

    def is_followed_by(self, user):
        """Check if another user has been signed for the current"""
        return Subscription.objects.filter(follower=user, following=self).exists()



class Subscription(models.Model):
    """
    Represents a subscription or "follow" relationship between two users.

    Attributes:
        follower (User): The user who is following another user.
        following (User): The user being followed by the follower.
        subscribed_at (datetime): The date and time when the subscription was created.

    Meta:
        unique_together (tuple): Ensures that a follower cannot follow the same user more than once.
        ordering (list): Orders subscriptions from the newest to the oldest, based on the subscription date.
    """
    follower = models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)  # The user who is signed
    following = models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)  # User to be signed
    subscribed_at = models.DateTimeField(default=now)  # When a subscription occurred

    class Meta:
        unique_together = ('follower', 'following')  # The user cannot subscribe to the same
        ordering = ['-subscribed_at']  # The latest subscriptions up

    def __str__(self):
        return f"{self.follower} -> {self.following}"
