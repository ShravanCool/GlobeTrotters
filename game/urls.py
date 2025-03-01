from django.urls import path
from game import views

urlpatterns = [
    path("", views.game_view, name="game_view"),
    path("submit/", views.submit_answer, name="submit_answer"),
    path("play-again/", views.play_again, name="play_again"),
]
