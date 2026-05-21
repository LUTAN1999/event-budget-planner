from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=300, blank=True)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_spent(self):
        return sum(cat.total_spent() for cat in self.categories.all())

    def remaining_budget(self):
        return self.total_budget - self.total_spent()


class Category(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    allocated_budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.event.name} - {self.name}"

    def total_spent(self):
        return sum(exp.amount for exp in self.expenses.all())

    def remaining(self):
        return self.allocated_budget - self.total_spent()

    def is_over_budget(self):
        return self.total_spent() > self.allocated_budget


class Expense(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"


class Vendor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='vendors')
    name = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)
    contact = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.name} - {self.service}"