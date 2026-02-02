from django.conf import settings
from django.db import models


class WorkoutCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "workout categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        WorkoutCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.category} - {self.date}"


class Exercise(models.Model):
    STRENGTH = "strength"
    CARDIO = "cardio"
    EXERCISE_TYPES = [
        (STRENGTH, "Strength"),
        (CARDIO, "Cardio"),
    ]

    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="exercises"
    )
    name = models.CharField(max_length=100)
    exercise_type = models.CharField(
        max_length=10, choices=EXERCISE_TYPES, default=STRENGTH
    )
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    distance = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ExerciseSet(models.Model):
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="sets"
    )
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ["set_number"]

    def __str__(self):
        return f"Set {self.set_number}: {self.reps} x {self.weight}"


class Meal(models.Model):
    MEAL_TYPES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(default=0)
    protein = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    carbs = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES, blank=True)
    notes = models.TextField(blank=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-logged_at"]

    def __str__(self):
        return f"{self.name} - {self.logged_at.date()}"


class SavedMeal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(default=0)
    protein = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    carbs = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=1, default=0)

    def __str__(self):
        return self.name


class WeighIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.weight} lbs - {self.date}"


class WaterIntake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    amount_oz = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique_water_per_day"
            )
        ]

    def __str__(self):
        return f"{self.amount_oz}oz - {self.date}"
