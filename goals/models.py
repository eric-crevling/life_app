from django.conf import settings
from django.db import models


class MacroGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=7, decimal_places=1)
    carbs = models.DecimalField(max_digits=7, decimal_places=1)
    fat = models.DecimalField(max_digits=7, decimal_places=1)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.calories} cal - starts {self.start_date}"


class WeightGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_weight = models.DecimalField(max_digits=5, decimal_places=1)
    target_date = models.DateField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.target_weight} lbs by {self.target_date}"


class StrengthGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    target_weight = models.DecimalField(max_digits=7, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.exercise_name}: {self.target_weight} lbs"
