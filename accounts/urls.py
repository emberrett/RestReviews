from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("activate/<uidb64>/<token>/",
         views.activate, name='activate'),
    path("account",
         views.view_account, name='view_account'),
    path("delete-account", views.delete_account, name="delete_account")
]
