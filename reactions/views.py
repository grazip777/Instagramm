# views.py
from django.db.models import F
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from post.models import Post
from reactions.models import Like, Dislike, Comment
from reactions.serializers import CommentSerializer


class LikeAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            # Если пользователь уже поставил лайк, удаляем его и уменьшаем счётчик
            existing_like.delete()
            Post.objects.filter(id=post_id).update(likes_count=F('likes_count') - 1)
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)

        # Удаляем дизлайк, если он есть, и увеличиваем счётчик лайков
        Dislike.objects.filter(user=user, post=post).delete()
        Like.objects.create(user=user, post=post)
        Post.objects.filter(id=post_id).update(likes_count=F('likes_count') + 1)
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
            # Если пользователь уже поставил дизлайк, удаляем его и уменьшаем счётчик
            existing_dislike.delete()
            Post.objects.filter(id=post_id).update(dislikes_count=F('dislikes_count') - 1)
            return Response({'message': 'Dislike removed'}, status=status.HTTP_200_OK)

        # Удаляем лайк, если он есть, и увеличиваем счётчик дизлайков
        Like.objects.filter(user=user, post=post).delete()
        Dislike.objects.create(user=user, post=post)
        Post.objects.filter(id=post_id).update(dislikes_count=F('dislikes_count') + 1)
        return Response({'message': 'Dislike added'}, status=status.HTTP_201_CREATED)

# Комментарий
class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Позволяем удалять комментарий только автору или админу
        user = self.request.user
        if user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(user=user)
