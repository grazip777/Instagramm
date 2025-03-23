from rest_framework import permissions, serializers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer



class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def filter_by_author(self, request):
        author_id = request.query_params.get('author_id')
        if author_id:
            queryset = self.get_queryset().filter(author_id=author_id)
            return queryset
        return self.get_queryset()


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        content = serializer.validated_data['content']
        serializer.save(author=self.request.user)



class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
