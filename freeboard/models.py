from django.db import models
from CustomUser.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    delete_unavailable = models.BooleanField(max_length=2, null=True)
    voter = models.ManyToManyField(User, related_name='voter_post')

    def __str__(self):
        return self.subject
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True,
                                 on_delete=models.CASCADE)