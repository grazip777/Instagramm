from django.db import models
from rest_framework.exceptions import ValidationError
from user.models import User

# Категория
class ReportCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Django не будет управлять таблицей в базе данных

# Жалоба
class Report(models.Model):
    category = models.ForeignKey(ReportCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.user == self.to:
            raise ValidationError("A user cannot report themselves.")
