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
