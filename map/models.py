from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(
        max_length=100,
    )

class Booth(models.Model):
    location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        max_length=100,
    )
    