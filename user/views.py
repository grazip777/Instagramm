from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.serializers import RegisterSerializer


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Вы прошли регистрацию, вам отправлено сообщение",
            "status": 200
        }, status=200)
    return Response(serializer.errors, status=400)

