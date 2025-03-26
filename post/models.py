from django.db import models
from rest_framework.authtoken.admin import User
from django.core.exceptions import ValidationError

# Пост
class Post(models.Model):

    photo = models.ImageField(upload_to='post_photo/', blank=True, null=True)
    video = models.FileField(upload_to='post_video/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comments_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} (Автор: {self.author.username})"





