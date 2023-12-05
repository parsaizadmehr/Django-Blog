from django.urls import path, include
from django.contrib.auth import views as auth_views # Django has the built in option for the login and logout
from . import views

# Serving files uploaded by a user during development
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="users\login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users\logout.html"), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
