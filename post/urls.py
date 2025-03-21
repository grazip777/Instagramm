from django.urls import path

from .views import PostCreateAPIView, PostListAPIView, PostUpdateAPIView, PostDeleteAPIView

urlpatterns = [
    # Create a new post.
    path('create/', PostCreateAPIView.as_view()),

    # List all posts.
    path('list/', PostListAPIView.as_view()),

    # Update a specific post by ID.
    path('update/<pk>/', PostUpdateAPIView.as_view()),

    # Delete a specific post by ID.
    path('delete/<pk>/', PostDeleteAPIView.as_view()),
]
