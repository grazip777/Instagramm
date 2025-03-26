from django.urls import path
from .views import LikeAPIView, DislikeAPIView
from django.urls import path
from .views import CommentCreateAPIView, CommentListAPIView, CommentDeleteAPIView, ReactionCreateAPIView, \
    ReactionDeleteAPIView

urlpatterns = [
    path('like/<int:post_id>/', LikeAPIView.as_view(), name='like'),
    path('dislike/<int:post_id>/', DislikeAPIView.as_view(), name='dislike'),
]


urlpatterns2 = [
    # Комментарии
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:post_id>/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/delete/<int:pk>/', CommentDeleteAPIView.as_view(), name='comment-delete'),
    # Реакции
    path('reactions/create/', ReactionCreateAPIView.as_view(), name='reaction-create'),
    path('reactions/delete/<int:pk>/', ReactionDeleteAPIView.as_view(), name='reaction-delete'),
]

urlpatterns = urlpatterns + urlpatterns2