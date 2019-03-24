from django.db import models


class Tag(models.Model):
    name = models.CharField(blank=False, max_length=200, unique=True)

    class Meta:
        db_table = 'tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
