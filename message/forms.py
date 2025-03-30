# forms.py

from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['to', 'message']
        labels = {
            'to': 'Получатель',
            'message': 'Сообщение',
        }
        widgets = {
            'to': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
