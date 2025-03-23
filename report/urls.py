from django.urls import path
from .views import ReportCategoryView

urlpatterns = [
    path('report/category/', ReportCategoryView.as_view(), name='category-list'),
    path('report/category/<int:pk>/', ReportCategoryView.as_view(), name='category-detail'),
]
