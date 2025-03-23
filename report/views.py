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


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ReportCategory
from .serializers import ReportCategorySerializer


class ReportCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = ReportCategory.objects.all()
        serializer = ReportCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ReportCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
