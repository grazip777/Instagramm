from django.urls import path
from report.views import CreateReportView, ReportCategoryView

urlpatterns = [
    path('send/', CreateReportView.as_view(), name='report'),
    path('category/', ReportCategoryView.as_view(), name='report-category'),
]