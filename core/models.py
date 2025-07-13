from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Technician', 'Technician'),
        ('Client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    CATEGORY_CHOICES = [
        ('Network', 'Network'),
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Other', 'Other'),
    ]

    CONNECTION_CHOICES = [
        ('Fibre', 'Fibre'),
        ('Wireless', 'Wireless'),
        ('Dont Know', 'Dont Know'),

    ]

    client_contact = models.CharField(max_length=100, default='Not Provided')
    location = models.CharField(max_length=255, default='Unknown')
    connection_type = models.CharField(max_length=20, choices=CONNECTION_CHOICES, default='Dont Know')
    account_number = models.CharField(max_length=100, default='N/A')
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_tickets', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    comments = models.TextField(blank=True, null=True)
    solved_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    