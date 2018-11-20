import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from apps.status.models import Status


class Project(models.Model):
    """ Project model """
    title = models.CharField(max_length=50)
    description = models.TextField()
    dead_line = models.DateField()
    created = models.DateField(default=datetime.date.today)
    slug = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title

    def user_has_permission(self, user):
        """ Verificando si un usuario tiene permisos para acceder al proyecto (editar) """
        return self.projectuser_set.filter(
            user = user, 
            permission_id__in = ProjectPermission.admin_permission()
            ).count() > 0

    def validate_unique(self, exclude=None):
        if Project.objects.filter(title=self.title).exclude(pk=self.id).exists():
            raise ValidationError("Ya hay un proyecto registrado con el mismo título")

    def get_id_status(self):
        return self.projectstatus_set.last().status_id

    def get_status(self):
        return self.projectstatus_set.last().status

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
    

class ProjectPermission(models.Model):
    """ Project permissions """
    title = models.CharField(max_length=50)
    description = models.TextField()
    level = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @classmethod
    def founder_permission(cls):
        return ProjectPermission.objects.get(pk=1)

    @classmethod
    def cofounder_permission(cls):
        return ProjectPermission.objects.get(pk=2)

    @classmethod
    def contributor_permission(cls):
        return ProjectPermission.objects.get(pk=3)

    @classmethod
    def admin_permission(cls):
        return [1 ,2]


class ProjectUser(models.Model):
    """ Project - User class """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, default=1)
    permission = models.ForeignKey(ProjectPermission)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.project.title)

    def get_project(self):
        return self.project

    def is_founder(self):
        return self.permission == ProjectPermission.founder_permission()

    def valid_change_permission(self):
        if not self.is_founder():
            return True
        return self.exist_founder()
        
    def exist_founder(self):
        return ProjectUser.objects.filter(
            project = self.project,
            permission = ProjectPermission.founder_permission()
        ).exclude(user=self.user).count() > 0
