from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from user.views import register, get_users, update_user_by_id, delete_user_by_id, SearchUserAPIView
from user.views import FollowUserView, UnfollowUserView, ListFollowersView, ListFollowingView

urlpatterns = [
    path('register/', register, name="register"),

    path('login/', TokenObtainPairView.as_view(), name="token"),

    path('get/', get_users, name="get-users"),

    path('update/<int:id>/', update_user_by_id, name="update-user"),

    path('delete/<int:id>/', delete_user_by_id, name="delete-user"),

    path('users/search/', SearchUserAPIView.as_view(), name='user-search'),

]

urlpatterns2 = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),

    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),

    path('followers/', ListFollowersView.as_view(), name='list-followers'),

    path('following/', ListFollowingView.as_view(), name='list-following'),
]

urlpatterns = urlpatterns + urlpatterns2
