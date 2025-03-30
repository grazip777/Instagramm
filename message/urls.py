from django.urls import path
from message import views
from message.views import *

urlpatterns = [
    path('create/', CreateMessageView.as_view(), name='create-message'),
    path('list/', ListAPIView.as_view(), name='list-message'),
    path('update/', UpdateAPIView.as_view(), name='update-message'),
    path('delete/', DestroyAPIView.as_view(), name='delete-message'),

]
urlpatterns2 = [
    path('send/', views.send_message, name='send_message'),
    path('messages/', views.messages_list, name='messages_list'),
]
urlpatterns = urlpatterns + urlpatterns2