from django.urls import path
from report.views import CreateReportView, CreateReportCategoryView

urlpatterns = [
    path('report/', CreateReportView.as_view(), name='report'),
    path('report/category/', CreateReportCategoryView.as_view(), name='report-category'),
]