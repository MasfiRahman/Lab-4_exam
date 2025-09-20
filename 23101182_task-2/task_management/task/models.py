from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()

    def _str_(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="tasks")

    def _str_(self):
        return self.title

    @property
    def days_left(self):
        """Calculated field: number of days left until due date"""
        return (self.due_date - timezone.now().date()).days

    def clean(self):
        """Custom validation: prevent assigning more than 5 pending tasks"""
        if self.status == "Pending":
            pending_tasks = Task.objects.filter(employee=self.employee, status="Pending")
            # Exclude current task if updating
            if self.pk:
                pending_tasks = pending_tasks.exclude(pk=self.pk)
            if pending_tasks.count() >= 5:
                raise ValidationError("This employee already has 5 pending tasks.")
