from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

class Post(models.Model):
    STATUS_CHOICES = [
        ("d", "Draft"),
        ("p", "Published"),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name="posts")
    thumbnail = models.ImageField(upload_to="uploads")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")
    
    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is empty
            self.slug = slugify(self.title)  # Generate slug from title
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.body} by {self.name}"