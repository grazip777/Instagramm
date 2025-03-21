from django.db import models
from rest_framework.authtoken.admin import User



class Post(models.Model):
    photo = models.ImageField(upload_to='post_photo/', blank=True, null=True) # фото является необязательным
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True) # контент явл. необязательным
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Автор: {self.User.username})" #приписание автора к посту