from django.db import models
from django.contrib.auth.models import User
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