from django.db import models
from rest_framework.authtoken.admin import User
from django.core.exceptions import ValidationError


class Post(models.Model):
    """
    Represents a blog post created by a user.

    Includes validation to ensure that either a photo or a video is provided,
    but not both at the same time, and at least one is required.
    """

    photo = models.ImageField(upload_to='post_photo/', blank=True, null=True)  # Optional photo
    video = models.FileField(upload_to='post_video/', blank=True, null=True)  # Optional video
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)  # Content is optional
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True, related_name='posts')

    def __str__(self):
        return f"{self.title} (Автор: {self.author.username})"

    def clean(self):
        """
        Custom validation to enforce the following rules:
        1. Either photo or video must be provided.
        2. Both photo and video cannot be provided at the same time.
        """
        super().clean()

        if self.photo and self.video:
            raise ValidationError('Вы не можете загрузить одновременно и фото, и видео.')

        if not self.photo and not self.video:
            raise ValidationError('Вы должны загрузить хотя бы фото или видео.')


class Hashtag(models.Model):
    """
    Model for hashtags.
    """
    name = models.CharField(max_length=50, unique=True)  # The name of the hashtag (unique)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
