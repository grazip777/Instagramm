from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from report.models import Report, ReportCategory
from report.serializers import ReportSerializer
from report.utils import send_to_telegram


class CreateReportView(CreateAPIView):  # Создание жалобы
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save()

        body = {
            "id": report.id,
            "user": report.user.username if report.user else "Anonymous",
            "to": report.to.username if report.to else "N/A",
            "reason": report.reason,
            "description": report.description,
            "created_at": str(report.created_at)
        }

        send_to_telegram(body)


class CreateReportCategoryView(CreateAPIView):
    queryset = ReportCategory.objects.all()
    serializer_class = ReportCategory
    permission_classes = [IsAdminUser]