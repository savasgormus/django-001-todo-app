from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    PRIORITY = (
        ("1", "High"),
        ("2", "Mid"),
        ("3", "Low"),
    )

    priority = models.CharField(max_length=10, choices=PRIORITY)
    isCompleted = models.BooleanField(default=False)

    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title