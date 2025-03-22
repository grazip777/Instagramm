from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from report.models import Report, ReportCategory
from report.serializers import ReportSerializer
from report.utils import send_to_telegram


class CreateReportView(CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save()

        body = {
            "id": report.id,
            "user": report.user.username,
            "to": report.to.username,
            "reason": report.category.name,
            "description": report.text,
            "created_at": str(report.created_at)
        }

        send_to_telegram(body)


class CreateReportCategoryView(CreateAPIView):
    queryset = ReportCategory.objects.all()
    serializer_class = ReportCategory
    permission_classes = [IsAdminUser]