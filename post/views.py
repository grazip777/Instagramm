from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import extract_hashtags
from .models import Post, Hashtag
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


class PostListCreateAPIView(APIView):
    """
    Class for creating and displaying the list of posts.
    """

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        content = data.get('content', '')  # We extract the content of the post

        # Automatically remove hashtags from the text
        hashtags = extract_hashtags(content)
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            post = serializer.save(author=request.user)  # We retain the post with the current author

            # Add the hashtags to the post
            for tag_name in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag_name.lower())
                post.hashtags.add(hashtag)

            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchByHashtagAPIView(APIView):
    """
    ЭInpoint for finding posts on a hashtag.
    """

    def get(self, request, hashtag_name, *args, **kwargs):
        try:
            hashtag = Hashtag.objects.get(name=hashtag_name.lower())  # We are looking for a hashtag by name
        except Hashtag.DoesNotExist:
            return Response({"detail": "Хештег не найден."}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(hashtags=hashtag)  # Find the posts associated with this hashtag
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


