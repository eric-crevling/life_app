from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from goals.models import MacroGoal, WeightGoal
from tracking.models import Meal, WaterIntake, WeighIn, Workout


@login_required
def home(request):
    today = timezone.localdate()
    user = request.user

    # Macro totals for today
    totals = Meal.objects.filter(
        user=user,
        logged_at__date=today,
    ).aggregate(
        total_calories=Sum("calories", default=0),
        total_protein=Sum("protein", default=0),
        total_carbs=Sum("carbs", default=0),
        total_fat=Sum("fat", default=0),
    )

    # Active macro goal
    macro_goal = MacroGoal.objects.filter(user=user, end_date__isnull=True).first()

    # Macro percentages for progress bars
    macro_progress = None
    if macro_goal:
        macro_progress = {
            "calories": (
                min(round(totals["total_calories"] / macro_goal.calories * 100), 100)
                if macro_goal.calories
                else 0
            ),
            "protein": (
                min(
                    round(
                        float(totals["total_protein"]) / float(macro_goal.protein) * 100
                    ),
                    100,
                )
                if macro_goal.protein
                else 0
            ),
            "carbs": (
                min(
                    round(float(totals["total_carbs"]) / float(macro_goal.carbs) * 100),
                    100,
                )
                if macro_goal.carbs
                else 0
            ),
            "fat": (
                min(
                    round(float(totals["total_fat"]) / float(macro_goal.fat) * 100), 100
                )
                if macro_goal.fat
                else 0
            ),
        }

    # Water
    water = WaterIntake.objects.filter(user=user, date=today).first()

    # Today's workouts
    todays_workouts = Workout.objects.filter(user=user, date=today)

    # Weight snapshot
    latest_weighin = WeighIn.objects.filter(user=user).first()
    weight_goal = WeightGoal.objects.filter(user=user, end_date__isnull=True).first()

    # Streak
    streak = 0
    check_date = today
    while True:
        has_meal = Meal.objects.filter(user=user, logged_at__date=check_date).exists()
        has_workout = Workout.objects.filter(user=user, date=check_date).exists()
        has_weighin = WeighIn.objects.filter(user=user, date=check_date).exists()
        if has_meal or has_workout or has_weighin:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return render(
        request,
        "dashboard/home.html",
        {
            "totals": totals,
            "macro_goal": macro_goal,
            "macro_progress": macro_progress,
            "water": water,
            "todays_workouts": todays_workouts,
            "latest_weighin": latest_weighin,
            "weight_goal": weight_goal,
            "streak": streak,
        },
    )
