from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from user.views import register, get_users, update_user_by_id, delete_user_by_id, SearchUserAPIView
from user.views import FollowUserView, UnfollowUserView, ListFollowersView, ListFollowingView

# User-related URLs
urlpatterns = [
    # POST: Create a new user account. URL: http://127.0.0.1:8000/user/register/
    path('register/', register, name="register"),

    # POST: Obtain a JWT token for authentication. URL: http://127.0.0.1:8000/user/login/
    path('login/', TokenObtainPairView.as_view(), name="token"),

    # GET: Retrieve a list of all users (admin only). URL: http://127.0.0.1:8000/user/get/
    path('get/', get_users, name="get-users"),

    # PUT: Update a user's information by ID. URL: http://127.0.0.1:8000/user/update/<id>/
    path('update/<int:id>/', update_user_by_id, name="update-user"),

    # DELETE: Remove a user by ID (admin only). URL: http://127.0.0.1:8000/user/delete/<id>/
    path('delete/<int:id>/', delete_user_by_id, name="delete-user"),

    # GET: Search for users by given query parameters. URL: http://127.0.0.1:8000/user/users/search/
    # Allows filtering based on various query parameters like username, etc.
    path('users/search/', SearchUserAPIView.as_view(), name='user-search'),

]

# Subscription-related URLs
urlpatterns2 = [
    # POST: Follow a user by ID. URL: http://127.0.0.1:8000/user/follow/<user_id>/
    # Requires authentication. Adds the specified user to the authenticated user's "following" list.
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),

    # DELETE: Unfollow a user by ID. URL: http://127.0.0.1:8000/user/unfollow/<user_id>/
    # Requires authentication. Removes the specified user from the authenticated user's "following" list.
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),

    # GET: Retrieve a list of the current user's followers. URL: http://127.0.0.1:8000/user/followers/
    # Requires authentication. Returns a list of users currently following the authenticated user.
    path('followers/', ListFollowersView.as_view(), name='list-followers'),

    # GET: Retrieve a list of the users the current user is following. URL: http://127.0.0.1:8000/user/following/
    # Requires authentication. Returns a list of users the authenticated user is currently following.
    path('following/', ListFollowingView.as_view(), name='list-following'),
]

# Combine urls into a single list
urlpatterns = urlpatterns + urlpatterns2
