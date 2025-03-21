# imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer


# User register
@api_view(["POST"]) # http://127.0.0.1:8000/user/register/
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Вы прошли регистрацию",
            "status": 200
        }, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])  # http://127.0.0.1:8000/user/get/
def get_users(request):
    data_from_db = User.objects.all()
    if len(data_from_db) == 0:
        return Response({"message": "Пользователи отсутствуют"}, status=200)
    serializer = UserProfileSerializer(data_from_db, many=True)
    return Response(serializer.data, status=200)


@api_view(["PUT"])  # http://127.0.0.1:8000/user/update/<id>/
def update_user_by_id(request, id):
    if not request.user.is_staff:  # Check if the user is an admin
        return Response({"error": "Доступ запрещен. Только администратор может"
                                  " выполнить данный запрос."
                                  "для запроса на изменение данных пишите на почту "
                                  "'Delt.6600@gmail.com'"}, status=403)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=404)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Информация пользователя обновлена."}, status=200)
    return Response(serializer.errors, status=400)
