from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import MealForm, WeighInForm, WorkoutCategoryForm, WorkoutForm
from .models import (
    Exercise,
    ExerciseSet,
    Meal,
    SavedMeal,
    WaterIntake,
    WeighIn,
    Workout,
    WorkoutCategory,
)


@login_required
@require_POST
def water_add(request):
    today = timezone.localdate()
    water, created = WaterIntake.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={"amount_oz": 0},
    )
    water.amount_oz += 8
    water.save()
    return render(request, "tracking/partials/water_display.html", {"water": water})


@login_required
def weighin_list(request):
    weighins = WeighIn.objects.filter(user=request.user)[:30]
    form = WeighInForm(initial={"date": timezone.localdate()})
    return render(
        request,
        "tracking/weighin_list.html",
        {
            "weighins": weighins,
            "form": form,
        },
    )


@login_required
@require_POST
def weighin_create(request):
    form = WeighInForm(request.POST)
    if form.is_valid():
        weighin = form.save(commit=False)
        weighin.user = request.user
        weighin.save()
        return render(
            request, "tracking/partials/weighin_row.html", {"weighin": weighin}
        )
    return HttpResponse(status=422)


def _get_today_totals(user):
    today = timezone.localdate()
    return Meal.objects.filter(
        user=user,
        logged_at__date=today,
    ).aggregate(
        total_calories=Sum("calories", default=0),
        total_protein=Sum("protein", default=0),
        total_carbs=Sum("carbs", default=0),
        total_fat=Sum("fat", default=0),
    )


def _check_overages(user, totals):
    from goals.models import MacroGoal

    goal = MacroGoal.objects.filter(user=user, end_date__isnull=True).first()
    if not goal:
        return []

    overages = []
    if totals["total_calories"] > goal.calories:
        over = totals["total_calories"] - goal.calories
        overages.append(f"{over} calories")
    if totals["total_protein"] > goal.protein:
        over = totals["total_protein"] - goal.protein
        overages.append(f"{over}g protein")
    if totals["total_carbs"] > goal.carbs:
        over = totals["total_carbs"] - goal.carbs
        overages.append(f"{over}g carbs")
    if totals["total_fat"] > goal.fat:
        over = totals["total_fat"] - goal.fat
        overages.append(f"{over}g fat")

    return overages


@login_required
def meal_list(request):
    today = timezone.localdate()
    meals = Meal.objects.filter(user=request.user, logged_at__date=today)
    totals = _get_today_totals(request.user)
    form = MealForm()
    return render(
        request,
        "tracking/meal_list.html",
        {
            "meals": meals,
            "totals": totals,
            "form": form,
        },
    )


@login_required
@require_POST
def meal_create(request):
    form = MealForm(request.POST)
    if form.is_valid():
        meal = form.save(commit=False)
        meal.user = request.user
        meal.save()
        totals = _get_today_totals(request.user)
        overages = _check_overages(request.user, totals)
        return render(
            request,
            "tracking/partials/meal_create_response.html",
            {
                "meal": meal,
                "totals": totals,
                "overages": overages,
            },
        )
    return HttpResponse(status=422)


@login_required
@require_POST
def meal_save(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    SavedMeal.objects.create(
        user=request.user,
        name=meal.name,
        calories=meal.calories,
        protein=meal.protein,
        carbs=meal.carbs,
        fat=meal.fat,
    )
    return render(
        request,
        "tracking/partials/meal_row.html",
        {
            "meal": meal,
            "just_saved": True,
        },
    )


@login_required
def saved_meal_list(request):
    saved_meals = SavedMeal.objects.filter(user=request.user)
    return render(
        request,
        "tracking/saved_meal_list.html",
        {
            "saved_meals": saved_meals,
        },
    )


@login_required
@require_POST
def saved_meal_relog(request, pk):
    saved = get_object_or_404(SavedMeal, pk=pk, user=request.user)
    Meal.objects.create(
        user=request.user,
        name=saved.name,
        calories=saved.calories,
        protein=saved.protein,
        carbs=saved.carbs,
        fat=saved.fat,
    )
    return render(
        request,
        "tracking/partials/saved_meal_row.html",
        {
            "saved": saved,
            "just_relogged": True,
        },
    )


@login_required
@require_POST
def saved_meal_delete(request, pk):
    saved = get_object_or_404(SavedMeal, pk=pk, user=request.user)
    saved.delete()
    return HttpResponse("")


@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)[:30]
    form = WorkoutForm(user=request.user, initial={"date": timezone.localdate()})
    category_form = WorkoutCategoryForm()
    return render(
        request,
        "tracking/workout_list.html",
        {
            "workouts": workouts,
            "form": form,
            "category_form": category_form,
        },
    )


@login_required
@require_POST
def workout_create(request):
    if "new_category" in request.POST:
        cat_form = WorkoutCategoryForm(request.POST)
        if cat_form.is_valid():
            cat = cat_form.save(commit=False)
            cat.user = request.user
            cat.save()
        return redirect("tracking:workout_list")

    form = WorkoutForm(request.POST, user=request.user)
    if form.is_valid():
        workout = form.save(commit=False)
        workout.user = request.user
        workout.save()
        return redirect("tracking:workout_detail", pk=workout.pk)
    return render(
        request,
        "tracking/workout_list.html",
        {
            "workouts": Workout.objects.filter(user=request.user)[:30],
            "form": form,
            "category_form": WorkoutCategoryForm(),
        },
    )


@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    exercises = workout.exercises.prefetch_related("sets").all()
    return render(
        request,
        "tracking/workout_detail.html",
        {
            "workout": workout,
            "exercises": exercises,
        },
    )


@login_required
@require_POST
def exercise_create(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    exercise = Exercise.objects.create(
        workout=workout,
        name=request.POST.get("name", ""),
        exercise_type=request.POST.get("exercise_type", "strength"),
        duration_minutes=request.POST.get("duration_minutes") or None,
        distance=request.POST.get("distance") or None,
    )
    return render(
        request, "tracking/partials/exercise_card.html", {"exercise": exercise}
    )


@login_required
@require_POST
def set_create(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, workout__user=request.user)
    last_set = exercise.sets.order_by("-set_number").first()
    next_number = (last_set.set_number + 1) if last_set else 1
    new_set = ExerciseSet.objects.create(
        exercise=exercise,
        set_number=next_number,
        reps=request.POST.get("reps", 0),
        weight=request.POST.get("weight", 0),
    )
    return render(request, "tracking/partials/set_row.html", {"set": new_set})


@login_required
@require_POST
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, workout__user=request.user)
    exercise.delete()
    return HttpResponse("")


@login_required
@require_POST
def set_delete(request, pk):
    exercise_set = get_object_or_404(
        ExerciseSet, pk=pk, exercise__workout__user=request.user
    )
    exercise_set.delete()
    return HttpResponse("")
