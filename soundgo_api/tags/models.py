from django.db import models


class Tag(models.Model):
    name = models.CharField(blank=False, max_length=200)
