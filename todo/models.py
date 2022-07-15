from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    PRIORITY = (
        ("High", "High"),
        ("Middle", "Mid"),
        ("Low", "Low"),
    )

    priority = models.CharField(max_length=50, choices=PRIORITY)
    isCompleted = models.BooleanField(default=False)

    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} {self.priority}"
