from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import uuid
import random
from game.models import Destination, Challenge
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
        else f"Incorrect! No points awarded. The correct answer is {correct_city}."
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


@login_required
def generate_challenge_link(request):
    invite_token = str(uuid.uuid4())[:8]
    Challenge.objects.create(
        inviter=request.user,
        invite_token=invite_token,
    )
    challenge_link = request.build_absolute_uri(f"/game/challenge/{invite_token}/")
    return render(request, "challenge_link.html", {"challenge_link": challenge_link})


def challenge_view(request, invite_token):
    challenge = get_object_or_404(Challenge, invite_token=invite_token)
    challenger_profile = UserProfile.objects.get(user=challenge.inviter)

    return render(
        request,
        "challenge_page.html",
        {
            "challenger_username": challenge.inviter.username,
            "challenger_score": challenger_profile.score,
        },
    )
