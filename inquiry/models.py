from django.db import models
from CustomUser.models import User

from django.template.defaultfilters import truncatechars
        
"""
Models starts here!
"""

class Post(models.Model):
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return (str(self.create_date) + "   "+ truncatechars(self.content, 30))
