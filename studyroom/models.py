from django.db import models
from CustomUser.models import User

class Room(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Reserve(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=200)
    year = models.CharField(max_length=200, null = True)
    month = models.CharField(max_length=200, null = True)
    day = models.CharField(max_length=200, null = True)
    date = models.IntegerField(null=True)
    room = models.CharField(max_length=200)

    def __str__(self):
        return self.room

