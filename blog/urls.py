from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path("post/<slug:slug>", views.post_detail, name="post"),
    path("new/", views.PostCreateView.as_view(), name="create"),
    path("post/<slug:slug>/update/", views.PostUpdateView.as_view(), name="update"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="delete"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
