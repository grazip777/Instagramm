from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import register

urlpatterns = [
    path("register/", register),
    path('login/', TokenObtainPairView.as_view()),
]