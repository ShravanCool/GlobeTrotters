from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from users.forms import UserRegistrationForm
from users.models import UserProfile


class SignupView(FormView):
    template_name = "signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("game_view")

    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Create a user profile
        profile = UserProfile.objects.create(user=user, score=0, games_played=0)
        messages.success(self.request, "Account created successfully!")

        # Log the user in
        login(self.request, user)

        # Initialize session variables
        self.request.session["score"] = profile.score
        self.request.session["games_played"] = profile.games_played

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating account. Please try again.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Initialize session variables
        profile = UserProfile.objects.get(user=user)
        self.request.session["score"] = profile.score
        self.request.session["games_played"] = profile.games_played

        messages.success(self.request, "Logged in successfully!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("game_view")


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("login")
