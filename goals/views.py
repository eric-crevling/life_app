from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import MacroGoalForm, StrengthGoalForm, WeightGoalForm
from .models import MacroGoal, StrengthGoal, WeightGoal


@login_required
def goal_overview(request):
    macro_goal = MacroGoal.objects.filter(
        user=request.user, end_date__isnull=True
    ).first()
    weight_goal = WeightGoal.objects.filter(
        user=request.user, end_date__isnull=True
    ).first()
    strength_goals = StrengthGoal.objects.filter(
        user=request.user, end_date__isnull=True
    )

    macro_form = MacroGoalForm(instance=macro_goal) if macro_goal else MacroGoalForm()
    weight_form = (
        WeightGoalForm(instance=weight_goal) if weight_goal else WeightGoalForm()
    )
    strength_form = StrengthGoalForm()

    return render(
        request,
        "goals/goal_overview.html",
        {
            "macro_goal": macro_goal,
            "weight_goal": weight_goal,
            "strength_goals": strength_goals,
            "macro_form": macro_form,
            "weight_form": weight_form,
            "strength_form": strength_form,
        },
    )


@login_required
@require_POST
def macro_goal_create(request):
    form = MacroGoalForm(request.POST)
    if form.is_valid():
        today = timezone.localdate()
        MacroGoal.objects.filter(user=request.user, end_date__isnull=True).update(
            end_date=today
        )
        goal = form.save(commit=False)
        goal.user = request.user
        goal.start_date = today
        goal.save()
        return redirect("goals:goal_overview")
    return render(
        request,
        "goals/goal_form.html",
        {
            "form": form,
            "title": "Set Macro Goals",
        },
    )


@login_required
@require_POST
def weight_goal_create(request):
    form = WeightGoalForm(request.POST)
    if form.is_valid():
        today = timezone.localdate()
        WeightGoal.objects.filter(user=request.user, end_date__isnull=True).update(
            end_date=today
        )
        goal = form.save(commit=False)
        goal.user = request.user
        goal.start_date = today
        goal.save()
        return redirect("goals:goal_overview")
    return render(
        request,
        "goals/goal_form.html",
        {
            "form": form,
            "title": "Set Weight Goal",
        },
    )


@login_required
@require_POST
def strength_goal_create(request):
    form = StrengthGoalForm(request.POST)
    if form.is_valid():
        today = timezone.localdate()
        StrengthGoal.objects.filter(
            user=request.user,
            end_date__isnull=True,
            exercise_name=form.cleaned_data["exercise_name"],
        ).update(end_date=today)
        goal = form.save(commit=False)
        goal.user = request.user
        goal.start_date = today
        goal.save()
        return redirect("goals:goal_overview")
    return render(
        request,
        "goals/goal_form.html",
        {
            "form": form,
            "title": "Set Strength Goal",
        },
    )
