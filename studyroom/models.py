from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Reserve(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=200)
    room = models.CharField(max_length=200)

    def __str__(self):
        return self.room
