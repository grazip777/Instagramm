
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User, Subscription
from user.serializers import RegisterSerializer, UserProfileSerializer, SubscriptionSerializer


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Вы прошли регистрацию",
            "status": 200
        }, status=200)
    return Response(serializer.errors, status=400)


# Get user
@api_view(['GET'])
def get_users(request):
    if not request.user.is_staff:
        data_from_db = User.objects.filter(is_staff=False)
        if len(data_from_db) == 0:
            return Response({"message": "Пользователей нету"}, status=200)
        serializer = UserProfileSerializer(data_from_db, many=True)
        return Response(serializer.data, status=200)
    elif request.user.is_staff:
        data_from_db = User.objects.all()
        if len(data_from_db) == 0:
            return Response({"message": "Пользователей нету"}, status=200)
        serializer = UserProfileSerializer(data_from_db, many=True)
        return Response(serializer.data, status=200)


@api_view(["PUT"])
def update_user_by_id(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=404)

    if request.user != user and not request.user.is_staff:
        return Response({"error": "Доступ запрещен. Вы можете обновить только свою учетную запись."}, status=403)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Информация пользователя обновлена."}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_user_by_id(request, id):
    if not request.user.is_staff:
        return Response({"error": "Доступ запрещен. Только администратор может выполнить данный запрос."}, status=403)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=404)
    user.delete()
    return Response({"message": "Пользователь удален!."}, status=200)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        to_follow_id = request.data.get('user_id')
        try:
            to_follow = User.objects.get(id=to_follow_id)
            request.user.follow(to_follow)  # Здесь вызывается метод follow()
            return Response({'success': 'Вы подписались на пользователя.'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=404)



class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, **kwargs):
        following_id = kwargs.get("user_id")
        try:
            following = User.objects.get(id=following_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        if following == request.user:
            return Response({"error": "Вы не можете отписаться от себя."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_staff:
            subscription = Subscription.objects.filter(follower=following, following=request.user)
        else:
            subscription = Subscription.objects.filter(follower=request.user, following=following)

        if subscription.exists():
            subscription.delete()
            return Response({"message": "Подписка успешна удалена."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Нет подписки на удаление."}, status=status.HTTP_400_BAD_REQUEST)


class ListFollowersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        followers = Subscription.objects.filter(following=request.user).order_by('-subscribed_at')
        serializer = SubscriptionSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = Subscription.objects.filter(follower=request.user).order_by('-subscribed_at')
        serializer = SubscriptionSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('username', '')
        if query:
            users = User.objects.filter(username__icontains=query)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Введите параметр username для запроса"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_emails(request):
    users = User.objects.all()
    emails = []
    for user in users:
        emails.append(user.email)
    return Response({"emails": emails}, status=200)
