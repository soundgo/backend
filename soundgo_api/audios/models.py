# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.



class Record(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    numberReproductions = models.IntegerField(validators=[MinValueValidator(0)])
    path = models.CharField(blank=True)



class Audio(Record):
    isInappropriate = models.BooleanField()
    timestampCreation = models.DateField(auto_now_add=True)
    timestampFinish = models.DateField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    site = models.ForeignKey("Site", blank=True, null=True, related_name='records')
    tags = models.ManyToManyField("Tag")


class Advertisement(Record):
    maxPriceToPay = models.FloatField(validators=[MinValueValidator(0)])
    radius = models.IntegerField(validators=[MinValueValidator(0)])
    isActive = models.BooleanField()
    isDelete = models.BooleanField()


class Category(models.Model):
    name = models.CharField(blank=True)
    maxTimeRecord = models.FloatField()
    minDurationMap = models.FloatField()


class Tag(models.Model):
    name = models.CharField(blank=True)


class Site(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(blank=True)
    description = models.CharField(blank=True)


