from django.db import models
from CustomUser.models import User


class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    end_date = models.DateTimeField()
    visible = models.BooleanField(max_length=2, null=True)

    def __str__(self):
        return self.subject
    
class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    post = models.ForeignKey(Post, null=True, blank=True,
                                 on_delete=models.SET_NULL)
