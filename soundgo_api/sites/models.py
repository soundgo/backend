from django.db import models


class Site(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(blank=False, max_length=200)
    description = models.CharField(blank=False, max_length=200)

    class Meta:
        db_table = 'site'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
