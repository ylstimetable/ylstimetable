from django.db import models
from CustomUser.models import User
from timetable.models import ClassD

class Assess(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    classinfo = models.ForeignKey(ClassD, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class ClassA(models.Model):
    subject = models.CharField(max_length=200)
    professor = models.CharField(max_length=200)
    semester = models.CharField(max_length=200)
    rate = models.CharField(max_length=200)
    
    def __str__(self):
        return self.subject

class ClassA_Post(models.Model):
    classinfo = models.ForeignKey(ClassA, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=True)
    professor = models.CharField(max_length=200, null=True)
    content = models.TextField()
    semester = models.CharField(max_length=200)
    create_date = models.DateTimeField(null=True)
    rate = models.CharField(max_length=200)

    def __str__(self):
        return self.subject
