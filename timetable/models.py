from django.db import models
from django.contrib.auth.models import User
from common.models import Profile

class ClassD(models.Model):
    title = models.CharField(max_length=200)
    professor = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    room = models.CharField(max_length=200)
    semester = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    ban = models.CharField(max_length=200)
    voter = models.ManyToManyField(User, related_name='class_voter', blank=True)

    def __str__(self):
        return self.title

class ClassM(models.Model):
    title = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    author = models.ManyToManyField(User, related_name='class_author', blank=True)

    def __str__(self):
        return self.title