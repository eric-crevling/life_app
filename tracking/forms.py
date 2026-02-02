from django import forms

from .models import Meal, WeighIn, Workout, WorkoutCategory


class WeighInForm(forms.ModelForm):
    class Meta:
        model = WeighIn
        fields = ["weight", "date"]
        widgets = {
            "weight": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "185.0",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input input-bordered w-full",
                }
            ),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "calories", "protein", "carbs", "fat", "meal_type"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. Chicken and rice",
                }
            ),
            "calories": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "0",
                }
            ),
            "protein": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "0",
                }
            ),
            "carbs": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "0",
                }
            ),
            "fat": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "0",
                }
            ),
            "meal_type": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
        }


class WorkoutCategoryForm(forms.ModelForm):
    class Meta:
        model = WorkoutCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. Push, Pull, Legs",
                }
            ),
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["category", "date", "notes"]
        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input input-bordered w-full",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 2,
                    "placeholder": "Optional notes",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = WorkoutCategory.objects.filter(user=user)
