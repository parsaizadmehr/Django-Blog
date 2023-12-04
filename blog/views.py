from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from decouple import config
from .models import Post, Category
from .forms import ContactUsForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Fetch all categories
        return context

    def get_queryset(self):
        return Post.objects.filter(status="p").order_by("-created_at")

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    context_object_name = "post"
    fields = ["title", "content", "thumbnail","categories", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    context_object_name = "post"
    fields = ["title", "content", "thumbnail","categories", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    categories  = post.categories.all()

    new_comment = None    # Comment posted
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "categories": categories,
        }
    return render(request, "blog/post.html", context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all()
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog/category_detail.html", context)

def about(request):
    return render(request, "blog/about.html")

@login_required
def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            
            try:
                send_mail(
                    f"New Contact Form Submission from {name}",
                    f"Message from {email}\n {message}",
                    config("EMAIL_HOST_USER"),
                    [config("RECIPIENT_EMAIL")],
                    fail_silently=False,
                )
                messages.success(request, f"{name}, Thanks for reaching us.")
                return redirect("index")
                
            except Exception as e:
                messages.warning(request, f"There was an error sending the email: {e}")
                
    else:
        form = ContactUsForm()
    return render(request, "blog/contact.html", {"form": form})