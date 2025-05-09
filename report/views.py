from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .utils import send_message
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ReportCategory, Report
from .serializers import ReportCategorySerializer, ReportSerializer

# Категория жалоб
class ReportCategoryView(APIView):
    def get(self, request, *args, **kwargs): # get category
        categories = ReportCategory.objects.all()
        serializer = ReportCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs): # create category
        serializer = ReportCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()

            # Телеграм сообщение
            message = f"Новая категория жалобы создана:\n\n" \
                      f"Название: {category.name}\n" \
                      f"Описание: {category.description}"

            # Отправка сообщение на телеграм
            send_message(message)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Создание репорта
class CreateReportView(CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Создание репорта
        report = serializer.save()

        # Телеграм сообщение
        message = (
            f"❗ Новая жалоба:\n\n"
            f"ID жалобы: {report.id}\n"
            f"Пользователь: {report.user.username}\n"
            f"Кому: {report.to.username}\n"
            f"Причина: {report.category.name}\n"
            f"Описание: {report.text}\n"
            f"Создано: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Отправка сообщение на телеграм
        send_message(message, report.category.name)
