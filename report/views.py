from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse  # Для генерации ссылки
from .models import ReportCategory
from .serializers import ReportCategorySerializer
from .utils import send_message


class ReportCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = ReportCategory.objects.all()
        serializer = ReportCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ReportCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()

            # Генерация ссылки на категорию
            # В примере я использую ваше API, но URL может быть связан с реальной страницей
            category_detail_url = request.build_absolute_uri(
                reverse('category-detail', kwargs={'pk': category.id})
            )

            # Формируем сообщение для Telegram
            message = f"Новая категория жалобы создана:\n\n" \
                      f"Название: {category.name}\n" \
                      f"Описание: {category.description}\n" \
                      f"Ссылка: {category_detail_url}"

            # Отправляем сообщение в Telegram
            send_message(message)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
