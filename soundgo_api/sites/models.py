from django.db import models
from accounts.models import Actor


class Site(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(blank=False, max_length=200)
    description = models.CharField(blank=False, max_length=200)
    actor = models.ForeignKey(Actor, null=False, on_delete=models.CASCADE, related_name='sites')

    class Meta:
        db_table = 'site'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
