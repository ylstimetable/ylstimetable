from django.db import models
from CustomUser.models import User

class Receipt(models.Model):
    semester = models.CharField(max_length=200)
    voter = models.ManyToManyField(User, related_name='voter', blank=True)
    month = models.CharField(max_length=2, null=True)
    day =models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.semester

class Reserve(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Reserve_author')
    room = models.CharField(max_length=200)

    def __str__(self):
        return self.room

class Result(models.Model):
    semester = models.CharField(max_length=200)
    sequence = models.TextField()
    sequence_backup = models.TextField(blank=True)
    current = models.CharField(max_length=200, blank=True)