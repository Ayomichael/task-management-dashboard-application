from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    STATUS_CHOICES = (
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Progress')
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    due_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title