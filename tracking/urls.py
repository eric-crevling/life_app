from django.urls import path

from . import views

app_name = "tracking"

urlpatterns = [
    # Workouts
    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/new/", views.workout_create, name="workout_create"),
    path("workouts/<int:pk>/", views.workout_detail, name="workout_detail"),
    path(
        "workouts/<int:pk>/add-exercise/", views.exercise_create, name="exercise_create"
    ),
    path("exercises/<int:pk>/add-set/", views.set_create, name="set_create"),
    path("exercises/<int:pk>/delete/", views.exercise_delete, name="exercise_delete"),
    path("sets/<int:pk>/delete/", views.set_delete, name="set_delete"),
    # Meals
    path("meals/", views.meal_list, name="meal_list"),
    path("meals/new/", views.meal_create, name="meal_create"),
    path("meals/saved/", views.saved_meal_list, name="saved_meal_list"),
    path("meals/<int:pk>/save/", views.meal_save, name="meal_save"),
    path(
        "meals/saved/<int:pk>/relog/", views.saved_meal_relog, name="saved_meal_relog"
    ),
    path(
        "meals/saved/<int:pk>/delete/",
        views.saved_meal_delete,
        name="saved_meal_delete",
    ),
    # Weigh-ins
    path("weigh-ins/", views.weighin_list, name="weighin_list"),
    path("weigh-ins/new/", views.weighin_create, name="weighin_create"),
    # Water
    path("water/add/", views.water_add, name="water_add"),
]
