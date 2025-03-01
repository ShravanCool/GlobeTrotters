import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from game.constants import (CORRECT_ANS_FEEDBACK, CORRECT_ANS_POINTS,
                            INCORRECT_ANS_FEEDBACK, INCORRECT_ANS_POINTS)
from game.models import Challenge, Destination
from users.models import UserProfile


@login_required
def game_view(request):
    # Select a random destination
    destination = Destination.get_random_destination()

    # Generate multiple-choice options
    choices = Destination.get_answer_choices(destination)

    # Store the correct answer in the session
    request.session["correct_city"] = destination.city
    request.session.modified = True

    context = {
        "clues": destination.clues,
        "choices": choices,
    }
    return render(request, "game.html", context)


@login_required
def submit_answer(request):
    selected_city = request.POST.get("answer")
    correct_city = request.session.get("correct_city")

    is_ans_correct = selected_city == correct_city
    feedback = (
        CORRECT_ANS_FEEDBACK
        if is_ans_correct
        else INCORRECT_ANS_FEEDBACK.format(correct_city=correct_city)
    )

    # Get the correct destination
    destination = Destination.objects.get(city=correct_city)

    # Get user profile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if is_ans_correct:
        profile.increment_score(CORRECT_ANS_POINTS)
    else:
        profile.increment_score(INCORRECT_ANS_POINTS)

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
