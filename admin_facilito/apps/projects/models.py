from django.db import models
from django.contrib.auth.models import User

import datetime


class Project(models.Model):
    """ Project model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    dead_line = models.DateField()
    created = models.DateField(default=datetime.date.today)


    def __str__(self):
        return self.title
    
