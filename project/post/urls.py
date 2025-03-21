from django.urls import path

from .views import PostCreateAPIView, PostListAPIView, PostUpdateAPIView, PostDeleteAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view()),
    path('list/', PostListAPIView.as_view()),
    path('update/<pk>/', PostUpdateAPIView.as_view()),
    path('delete/<pk>/', PostDeleteAPIView.as_view()),
]