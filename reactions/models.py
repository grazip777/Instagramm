from django.db import models
from user.models import User
from post.models import Post


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-timestamp']

    def __str__(self):
        return f"Dislike by {self.user.username} on post {self.post.id}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-timestamp']

    def __str__(self):
        return f"Like by {self.user.username} on post {self.post.id}"





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Связь с постом
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    text = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f"Комментарий от {self.author.username} для поста {self.post.title}"


class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')  # Связь с постом
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор реакции
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)  # Тип реакции (лайк/дизлайк)

    def __str__(self):
        return f"{self.reaction_type.capitalize()} от {self.user.username} для поста {self.post.title}"

    class Meta:
        unique_together = ('post', 'user')  # Каждый пользователь может оставить только одну реакцию на пост
