from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    GENDER_CHOICE = [
        ("m", "Male"),
        ("f", "Female"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="users/default.jpg", upload_to="users")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    joined_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} Profile"