from django.db import models
from rest_framework.authtoken.admin import User
from django.core.exceptions import ValidationError


# post/models.py

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    photo = models.ImageField(upload_to='post_photo/', blank=True, null=True)
    video = models.FileField(upload_to='post_video/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def comment_count(self):
        # Подсчет комментариев из связанных данных
        return self.comments.count()

    @property
    def like_count(self):
        # Подсчет лайков из связанных данных
        return self.reactions.filter(reaction_type='like').count()

    @property
    def dislike_count(self):
        # Подсчет дизлайков из связанных данных
        return self.reactions.filter(reaction_type='dislike').count()

    def __str__(self):
        return f"{self.title} (Автор: {self.author.username})"





