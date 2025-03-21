from django.db import models
from rest_framework.authtoken.admin import User


class Post(models.Model):
    """
    Represents a blog post created by a user.

    Fields:
        photo (ImageField): An optional photo associated with the post. Stored in 'post_photo/' directory.
        author (ForeignKey): The user who created the post. Linked to the User model.
        title (CharField): The title of the post with a maximum length of 50 characters.
        content (TextField): The content or body of the post (optional).
        created_at (DateTimeField): The date and time when the post was created (auto-generated).
    """
    photo = models.ImageField(upload_to='post_photo/', blank=True, null=True)  # The photo is optional
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)  # Content is clear optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Автор: {self.author.username})"  # author's attribution to post
