from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
from game.models import Destination
from users.models import UserProfile


@login_required
def game_view(request):
    # Select a random destination
    destination = random.choice(Destination.objects.all())

    # Generate multiple-choice options
    choices = [destination.city] + [
        d.city
        for d in random.sample(list(Destination.objects.exclude(id=destination.id)), 3)
    ]
    random.shuffle(choices)

    # Store the correct answer in the session
    request.session["correct_city"] = destination.city
    request.session.modified = True

    context = {
        "clues": destination.clues,  # Show both clues initially
        "choices": choices,
    }
    return render(request, "game.html", context)


@login_required
def submit_answer(request):
    selected_city = request.POST.get("answer")
    correct_city = request.session.get("correct_city")

    is_ans_correct = selected_city == correct_city
    feedback = (
        "Correct! You scored 3 points."
        if is_ans_correct
        else "Incorrect! No points awarded."
    )

    # Get the correct destination
    destination = Destination.objects.get(city=correct_city)

    # Get user profile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if is_ans_correct:
        profile.increment_score(3)
    else:
        profile.increment_score(0)

    profile.refresh_from_db()
    # Update the session score and games played
    request.session["score"] = profile.score
    request.session["games_played"] = profile.games_played
    request.session.modified = True

    return JsonResponse(
        {
            "correct": is_ans_correct,
            "feedback": feedback,
            "score": profile.score,
            "games_played": profile.games_played,
            "fun_fact": destination.get_random_fun_fact(),
            "trivia": destination.get_random_trivia(),
        }
    )


@login_required
def play_again(request):
    return redirect("game_view")
