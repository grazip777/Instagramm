from django.urls import path
from .views import LikeAPIView, DislikeAPIView

urlpatterns = [
    path('like/<int:post_id>/', LikeAPIView.as_view(), name='like'),
    path('dislike/<int:post_id>/', DislikeAPIView.as_view(), name='dislike'),
]
