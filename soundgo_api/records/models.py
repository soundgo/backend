from django.db import models

from django.core.validators import MinValueValidator

from sites.models import Site
from tags.models import Tag


class Record(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    numberReproductions = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    path = models.CharField(blank=False, max_length=200)


class Audio(Record):
    isInappropriate = models.BooleanField(default=False)
    timestampCreation = models.DateField(auto_now_add=True, editable=False)
    timestampFinish = models.DateField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    site = models.ForeignKey(Site, null=True, related_name='records', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class Advertisement(Record):
    maxPriceToPay = models.FloatField(validators=[MinValueValidator(0)])
    radius = models.IntegerField(validators=[MinValueValidator(0)])
    isActive = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(blank=False, max_length=200)
    maxTimeRecord = models.FloatField(default=60)
    minDurationMap = models.FloatField(default=259200)
