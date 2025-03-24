from .views import *
from django.urls import path

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post-create'), # Создание постов
    path('list/', PostListAPIView.as_view(), name='post-list'), # Получение постов
    path('update/<pk>/', PostUpdateAPIView.as_view(), name='post-update'), # Изменение постов
    path('delete/<pk>/', PostDeleteAPIView.as_view(), name='post-delete'), # Удаление постов
]