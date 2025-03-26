from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Like, Dislike, Post


class LikeAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            existing_like.delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)

        Dislike.objects.filter(user=user, post=post).delete()
        Like.objects.create(user=user, post=post)
        return Response({'message': 'Like added'}, status=status.HTTP_201_CREATED)


class DislikeAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        existing_dislike = Dislike.objects.filter(user=user, post=post).first()
        if existing_dislike:
            existing_dislike.delete()
            return Response({'message': 'Dislike removed'}, status=status.HTTP_200_OK)

        Like.objects.filter(user=user, post=post).delete()
        Dislike.objects.create(user=user, post=post)
        return Response({'message': 'Dislike added'}, status=status.HTTP_201_CREATED)

# reactions/views.py
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Reaction
from .serializers import CommentSerializer, ReactionSerializer
from post.models import Post


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Сохраняем автора как текущего пользователя


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Получаем пост по id и возвращаем только связанные с ним комментарии
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

# reactions/views.py

class ReactionCreateAPIView(CreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Сохраняем пользователя


class ReactionDeleteAPIView(DestroyAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]
