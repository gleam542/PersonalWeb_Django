from django.db import models
from django.utils import timezone

class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()

class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name