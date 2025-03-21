from django.urls import path
from views.views import TokenObtainPairView

from .serializers import MyTokenObtainPairView
from .views import register, get_users, update_user_by_id


urlpatterns = [
    path('register/', register, name="register"),
    path('login/', MyTokenObtainPairView.as_view(), name="token"),
    path('get/', get_users, name="get-users"),
    path('update/<int:id>/', update_user_by_id, name="get-user"),
]