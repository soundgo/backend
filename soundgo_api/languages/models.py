from django.db import models


class Language(models.Model):
    name = models.CharField('Name', max_length=200)

    class Meta:
        db_table = 'language'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return "%s" % self.name
