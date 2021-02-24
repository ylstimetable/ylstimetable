from django.db import models
from django.contrib.auth.models import User

class Announce(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_announce')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_announce')

    def __str__(self):
        return self.subject