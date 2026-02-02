from django.contrib import admin

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


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


class ExerciseSetInline(admin.TabularInline):
    model = ExerciseSet
    extra = 3


@admin.register(WorkoutCategory)
class WorkoutCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("date", "category", "user")
    list_filter = ("date", "category")
    inlines = [ExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "exercise_type", "workout")
    list_filter = ("exercise_type",)
    inlines = [ExerciseSetInline]


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "calories",
        "protein",
        "carbs",
        "fat",
        "meal_type",
        "logged_at",
    )
    list_filter = ("meal_type", "logged_at")


@admin.register(SavedMeal)
class SavedMealAdmin(admin.ModelAdmin):
    list_display = ("name", "calories", "protein", "carbs", "fat", "user")


@admin.register(WeighIn)
class WeighInAdmin(admin.ModelAdmin):
    list_display = ("weight", "date", "user")
    list_filter = ("date",)


@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ("amount_oz", "date", "user")
    list_filter = ("date",)
