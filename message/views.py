from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from message.models import Message
from message.serializers import MessageSerializer

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CreateMessageView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

class MessageListView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser]

class MessageDestroyView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser]

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messages_list')  # Перенаправление после успешной отправки
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})


@login_required
def messages_list(request):
    # Получить отправленные и полученные сообщения текущего пользователя
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(to=request.user)
    return render(request, 'messages_list.html', {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    })
