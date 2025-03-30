from django.db import models
from django.core.exceptions import ValidationError


class Message(models.Model):
    sender = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sender')
    message = models.TextField(max_length=100)
    to = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='to')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def validate(self):
        if self.sender == self.to:
            raise ValidationError("Вы не можете отправить сообщение самому себе!")



