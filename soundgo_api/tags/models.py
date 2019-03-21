from django.db import models


class Tag(models.Model):
    name = models.CharField(blank=True, max_length=200)
