from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from users.forms import UserRegistrationForm
from users.models import UserProfile


def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(user=user, score=0, games_played=0)
            messages.success(request, "Account created successfully!")

            login(request, user)

            # Initialize session variables
            request.session["score"] = profile.score
            request.session["games_played"] = profile.games_played

            return redirect("game_view")
        else:
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = UserRegistrationForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Initialize session variables
            profile = UserProfile.objects.get(user=user)
            request.session["score"] = profile.score
            request.session["games_played"] = profile.games_played

            print("Point 1")

            messages.success(request, "Logged in successfully!")
            return redirect("game_view")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("game_view")
