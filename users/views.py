from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserInfoForm, ProfileForm
from .models import Profile

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            profile = user.profile  # Get or create the user's profile
            profile.gender = form.cleaned_data['gender']
            profile.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"{username}, your account was created.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    
    return render(request, "users/register.html", {"form": form})

@login_required
def profile(request):
    
    if request.method == "POST":
        u_form = UserInfoForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your Profile Have Been Updated.")
            return redirect("profile")

    else:
        u_form = UserInfoForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "users/profile.html", context)