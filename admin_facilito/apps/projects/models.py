import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from apps.status.models import Status


class Project(models.Model):
    """ Project model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    dead_line = models.DateField()
    created = models.DateField(default=datetime.date.today)
    slug = models.CharField(max_length=50, default='')


    def __str__(self):
        return self.title


    def validate_unique(self, exclude=None):
        if Project.objects.filter(title=self.title).exists():
            raise ValidationError("Ya hay un proyecto registrado con el mismo título")


    def save(self, *args, **kwargs):
        self.validate_unique()
        self.slug = self.title.replace(' ', '-').lower()
        super(Project, self).save(*args, **kwargs)
    

class ProjectStatus(models.Model):
    project = models.ForeignKey(Project)
    status = models.ForeignKey(Status)
    created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.project.title
    
