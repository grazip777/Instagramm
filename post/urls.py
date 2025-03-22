from .views import *
from django.urls import path

urlpatterns = [
    # Create a new post.
    path('create/', PostCreateAPIView.as_view(), name='post-create'),  # Endpoint to create a new post.

    # List all posts.
    path('list/', PostListAPIView.as_view(), name='post-list'),  # Endpoint to list all available posts.

    # Update a specific post by ID.
    path('update/<pk>/', PostUpdateAPIView.as_view(), name='post-update'),
    # Endpoint to update an existing post by its ID.

    # Delete a specific post by ID.
    path('delete/<pk>/', PostDeleteAPIView.as_view(), name='post-delete'),
    # Endpoint to delete an existing post by its ID.
]


urlpatterns2 = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    # Endpoint to list posts or create a new post.
    path('posts/hashtag/<str:hashtag_name>/', SearchByHashtagAPIView.as_view(), name='search-by-hashtag'),
    # Endpoint to search posts by hashtag name.
]
urlpatterns = urlpatterns + urlpatterns2
