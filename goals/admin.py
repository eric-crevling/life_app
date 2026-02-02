from django.contrib import admin

from .models import MacroGoal, StrengthGoal, WeightGoal


@admin.register(MacroGoal)
class MacroGoalAdmin(admin.ModelAdmin):
    list_display = (
        "calories",
        "protein",
        "carbs",
        "fat",
        "start_date",
        "end_date",
        "user",
    )
    list_filter = ("start_date",)


@admin.register(WeightGoal)
class WeightGoalAdmin(admin.ModelAdmin):
    list_display = ("target_weight", "target_date", "start_date", "end_date", "user")


@admin.register(StrengthGoal)
class StrengthGoalAdmin(admin.ModelAdmin):
    list_display = ("exercise_name", "target_weight", "start_date", "end_date", "user")
