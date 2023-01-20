from django.urls import path

from users.views import user_views

urlpatterns = [
    path("", user_views.UsersView.as_view(), name="user_list"),
    path("<int:pk>/", user_views.UserDetailView.as_view(), name="user_detail_info"),
    path("create/", user_views.UserCreateView.as_view(), name="create_user"),
    path("<int:pk>/update/", user_views.UserUpdateView.as_view(), name="update_user"),
    path("<int:pk>/delete/", user_views.UserDeleteView.as_view(), name="delete_user"),
    ]
