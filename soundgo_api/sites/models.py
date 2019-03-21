from django.db import models


class Site(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)
