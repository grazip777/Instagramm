from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from user.views import register, get_users, update_user_by_id, delete_user_by_id, SearchUserAPIView, get_emails, \
    get_user_by_id, SendCodeAPIView, VerifyCodeAPIView
from user.views import FollowUserView, UnfollowUserView, ListFollowersView, ListFollowingView

# Ссылки пользователей
urlpatterns = [
    path('register/', register, name="register"), # Регистрация
    path('login/', TokenObtainPairView.as_view(), name="login"), # Логин
    path('get/users/<pk>/', get_user_by_id, name="get-user"), # Получение пользователя
    path('get/users/', get_users, name="get-users"), # Получение пользователей
    path('update/<int:id>/', update_user_by_id, name="update-user"), # Изменить данные пользователя
    path('delete/<int:id>/', delete_user_by_id, name="delete-user"), # Удалить данные пользователя
    path('users/search/', SearchUserAPIView.as_view(), name='user-search'), # Получение по username
    path('get/emails/', get_emails, name='get-emails'), # Получение email всех пользователей
    path('send-code/', SendCodeAPIView.as_view(), name='send_code'),
    path('verify-code/', VerifyCodeAPIView.as_view(), name='verify_code'),

]

# Ссылки подписок
urlpatterns2 = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'), # Подписаться
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'), # Отписаться
    path('followers/', ListFollowersView.as_view(), name='list-followers'), # Подписчики
    path('following/', ListFollowingView.as_view(), name='list-following'), # Подписки
]

urlpatterns = urlpatterns + urlpatterns2 # Метод
