# imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User, Subscription
from user.serializers import RegisterSerializer, UserProfileSerializer, SubscriptionSerializer


# Register user
@api_view(["POST"])  # http://127.0.0.1:8000/user/register/
def register(request):
    """
    Registers a new user in the system.

    Accepts a POST request with user registration data (email, password, and avatar).
    Validates the inputs and creates a new user if the data is valid.

    Returns:
        - 200: Registration successful with a success message.
        - 400: Validation errors in the submitted data.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Вы прошли регистрацию",
            "status": 200
        }, status=200)
    return Response(serializer.errors, status=400)

# Get user
@api_view(['GET'])  # http://127.0.0.1:8000/user/get/
def get_users(request):
    """
    Retrieves a list of all registered users.

    This endpoint is only accessible to admin users. If there are no users in the
    database, returns a message saying so. Otherwise, returns serialized user data.

    Returns:
        - 200: List of all users (if any) or a message indicating no users exist.
        - 403: Access denied, user is not an admin.
    """
    if not request.user.is_staff:  # Check if the user is an admin
        return Response({"error": "Доступ запрещен. Только администратор может выполнить данный запрос."}, status=403)
    data_from_db = User.objects.all()
    if len(data_from_db) == 0:
        return Response({"message": "Пользователей нету"}, status=200)
    serializer = UserProfileSerializer(data_from_db, many=True)
    return Response(serializer.data, status=200)

# Update user
@api_view(["PUT"])  # http://127.0.0.1:8000/user/update/<id>/
def update_user_by_id(request, id):
    """
    Updates user information for a specific user by ID.

    Accepts a PUT request with updated user data. Only accessible to the user being
    updated or an admin user. Validates the inputs and updates the user if valid.

    Args:
        id (int): The ID of the user to update.

    Returns:
        - 200: User information successfully updated.
        - 400: Validation errors in the submitted data.
        - 403: Access denied, the user does not have permission to update this account.
        - 404: User not found.
    """
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=404)

    # Allow updates only for the owner of the account or an admin
    if request.user != user and not request.user.is_staff:
        return Response({"error": "Доступ запрещен. Вы можете обновить только свою учетную запись."}, status=403)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Информация пользователя обновлена."}, status=200)
    return Response(serializer.errors, status=400)

# Delete user
@api_view(['DELETE'])
def delete_user_by_id(request, id): # http://127.0.0.1:8000/user/delete/<int:id>/
    """
    Deletes a user by their ID.

    This endpoint is only accessible to admin users. Attempts to delete the user
    if they exist in the database.

    Args:
        id (int): The ID of the user to delete.

    Returns:
        - 200: User successfully deleted.
        - 403: Access denied, user is not an admin.
        - 404: User not found.
    """
    if not request.user.is_staff:  # Check if the user is an admin
        return Response({"error": "Доступ запрещен. Только администратор может выполнить данный запрос."}, status=403)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=404)
    user.delete()
    return Response({"message": "Пользователь удален!."}, status=200)




class FollowUserView(APIView):
    """
    Subscribe to another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following_id = kwargs.get("user_id")  # Get the ID of the user to follow
        try:
            following = User.objects.get(id=following_id)  # Fetch the user object
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Prevent users from following themselves
        if following == request.user:
            return Response({"error": "Вы не можете подписаться сами на себя."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a subscription or check if it already exists
        subscription, created = Subscription.objects.get_or_create(
            follower=request.user,
            following=following
        )
        if not created:
            return Response({"error": "Вы уже подписаны на этого пользователя."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the subscription data
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    """
    Unfollow another user or delete a subscriber (for admins).
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        following_id = kwargs.get("user_id")  # Get the ID of the user to unfollow
        try:
            following = User.objects.get(id=following_id)  # Fetch the user object
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Prevent users from unfollowing themselves
        if following == request.user:
            return Response({"error": "Вы не можете отписаться от себя."}, status=status.HTTP_400_BAD_REQUEST)

        # Admins can delete followers, regular users can only delete their own subscriptions
        if request.user.is_staff:  # Check for admin privileges
            subscription = Subscription.objects.filter(follower=following, following=request.user)
        else:  # Regular user: filter by their own subscriptions
            subscription = Subscription.objects.filter(follower=request.user, following=following)

        if subscription.exists():
            # Delete the subscription if it exists
            subscription.delete()
            return Response({"message": "Подписка успешна удалена."}, status=status.HTTP_204_NO_CONTENT)

        # If no subscription is found, return an error response
        return Response({"error": "Нет подписки на удаление."}, status=status.HTTP_400_BAD_REQUEST)


class ListFollowersView(APIView):
    """
    List all followers of the current user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all users who follow the current user
        followers = Subscription.objects.filter(following=request.user).order_by('-subscribed_at')
        serializer = SubscriptionSerializer(followers, many=True)  # Serialize the results
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListFollowingView(APIView):
    """
    List all users the current user is following.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all users the current user is following
        following = Subscription.objects.filter(follower=request.user).order_by('-subscribed_at')
        serializer = SubscriptionSerializer(following, many=True)  # Serialize the results
        return Response(serializer.data, status=status.HTTP_200_OK)

