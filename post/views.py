from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


class PostListAPIView(ListAPIView):
    """
    API view to retrieve a list of posts.
    
    This view applies authentication and owner-based permissions. It optionally
    filters posts by the author ID if provided in the request parameters.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Authentication check
    def filter_by_author(self, request):
        """
        Filters the queryset of posts by the author's ID.

        Args:
            request (Request): The HTTP request object containing query parameters.

        Returns:
            QuerySet: Filtered list of posts authored by a specific user or the full
            queryset if no filter is applied.
        """
        author_id = request.query_params.get('author_id')
        if author_id:
            queryset = self.get_queryset().filter(author_id=author_id)
            return queryset
        return self.get_queryset()


class PostCreateAPIView(CreateAPIView):
    """
    API view to create a new post.
    
    Authentication is required, and the author's username is automatically 
    assigned to the post based on the logged-in user.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Authentication check

    def perform_create(self, serializer):
        """
        Handles setting the author of the post to the currently logged-in user.

        Args:
            serializer (Serializer): The serializer instance for the post model.
        """
        serializer.save(author=self.request.user)
        # Automatic filling of the author's field


class PostUpdateAPIView(UpdateAPIView):
    """
    API view to update an existing post.

    Authentication and ownership are required to perform updates. Only post
    owners and authenticated users with the necessary permissions can update
    a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Authentication check


class PostDeleteAPIView(DestroyAPIView):
    """
    API view to delete a post.

    Authentication and ownership are required to delete posts. Only post
    owners and users with appropriate permissions can delete a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Authentication check
