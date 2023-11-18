from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Post.objects.filter(status="p")
    
class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post.html"
