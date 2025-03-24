from django.urls import path
from .views import CreateReportView, ReportCategoryView

urlpatterns = [
    # Маршрут для создания жалоб
    path('report/', CreateReportView.as_view(), name='create-report'), #

    # Маршруты для работы с категориями жалоб
    path('report/category/', ReportCategoryView.as_view(), name='category-list'),
    path('report/category/<int:pk>/', ReportCategoryView.as_view(), name='category-detail'),
]
