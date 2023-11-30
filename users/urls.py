from django.urls import path
from django.contrib.auth import views as auth_views # Django has the built in option for the login and logout
from . import views

# Serving files uploaded by a user during development
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="users\login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users\logout.html"), name="logout"),
    path("profile/", views.profile, name="profile")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
