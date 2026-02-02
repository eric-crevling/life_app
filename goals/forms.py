from django import forms

from .models import MacroGoal, StrengthGoal, WeightGoal


class MacroGoalForm(forms.ModelForm):
    class Meta:
        model = MacroGoal
        fields = ["calories", "protein", "carbs", "fat"]
        widgets = {
            "calories": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "2000",
                }
            ),
            "protein": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "150",
                }
            ),
            "carbs": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "200",
                }
            ),
            "fat": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "65",
                }
            ),
        }


class WeightGoalForm(forms.ModelForm):
    class Meta:
        model = WeightGoal
        fields = ["target_weight", "target_date"]
        widgets = {
            "target_weight": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "175.0",
                }
            ),
            "target_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input input-bordered w-full",
                }
            ),
        }


class StrengthGoalForm(forms.ModelForm):
    class Meta:
        model = StrengthGoal
        fields = ["exercise_name", "target_weight"]
        widgets = {
            "exercise_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. Bench Press",
                }
            ),
            "target_weight": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.1",
                    "placeholder": "225",
                }
            ),
        }
