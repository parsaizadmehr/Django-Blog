from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path("post/<slug:slug>", views.post_detail, name="post"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
