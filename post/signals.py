# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from reactions.models import Comment
from .models import Post


# Увеличиваем счетчик комментариев при создании комментария
@receiver(post_save, sender=Comment)
def increase_comment_count(sender, instance, created, **kwargs):
    if created:
        Post.objects.filter(id=instance.post.id).update(comments_count=F('comments_count') + 1)


# Уменьшаем счетчик комментариев при удалении комментария
@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    Post.objects.filter(id=instance.post.id).update(comments_count=F('comments_count') - 1)
