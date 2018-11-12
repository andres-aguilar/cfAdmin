from django.db import models
from django.utils import timezone

# Create your models here.
class Status(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    color = models.CharField(max_length=10)
    created = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_default_status(cls):
        return cls.objects.get(pk=1)

    class Meta:
        verbose_name_plural = 'status'


