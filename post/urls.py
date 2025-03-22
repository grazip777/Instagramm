from .views import *
from django.urls import path

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('list/', PostListAPIView.as_view(), name='post-list'),
    path('update/<pk>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('delete/<pk>/', PostDeleteAPIView.as_view(), name='post-delete'),
]