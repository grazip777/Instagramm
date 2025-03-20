from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import register, get_users, update_user_by_id

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', TokenObtainPairView.as_view(), name="token"),
    path('get/', get_users, name="get-users"),
    path('update/<int:id>/', update_user_by_id, name="get-user"),
]