from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import accountsView, RegisterView, UserListView, ProfileView, UserDetailView, LogoutView, LoginView, LogoutAPIView, SignUpView, UserListHtmlView, UserEditView, UserDeleteView, ProfileHtmlView


urlpatterns = [
    path("", accountsView, name="accounts"),
    path("register/", RegisterView.as_view(), name="register"),
    path("register/html", SignUpView.as_view(), name="sign_up_html"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/html/", LoginView.as_view(), name="login_html"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/html", UserListHtmlView.as_view(), name="user_list_html"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/", UserEditView.as_view(), name="user_edit_html"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/html/", ProfileHtmlView.as_view(), name="profile_html"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("logout/html/", LogoutView.as_view(), name="logout_html"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete_html"),

]
