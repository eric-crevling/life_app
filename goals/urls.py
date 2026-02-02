from django.urls import path

from . import views

app_name = "goals"

urlpatterns = [
    path("", views.goal_overview, name="goal_overview"),
    path("macros/new/", views.macro_goal_create, name="macro_goal_create"),
    path("weight/new/", views.weight_goal_create, name="weight_goal_create"),
    path("strength/new/", views.strength_goal_create, name="strength_goal_create"),
]
