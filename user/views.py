# imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from user.serializers import RegisterSerializer, UserProfileSerializer


# User register
@api_view(["POST"]) # http://127.0.0.1:8000/user/register/
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Вы прошли регистрацию, вам отправлено сообщение",
            "status": 200
        }, status=200)
    return Response(serializer.errors, status=400)

@api_view(['GET']) # http://127.0.0.1:8000/user/register/
def get_users(request):
    data_from_db = User.objects.all()
    if len(data_from_db) == 0:
        return Response({"message": "Пользователей нетуу"}, status=200)
    serializer = UserProfileSerializer(data_from_db, many=True)
    return Response(serializer.data, status=200)