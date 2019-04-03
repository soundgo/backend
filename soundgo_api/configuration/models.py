from django.db import models


class Configuration(models.Model):
    maximum_radius = models.PositiveIntegerField('Maximum Radius (m)', default=2000)
    minimum_radius = models.PositiveIntegerField('Minimum Radius (m)', default=20)
    time_listen_advertisement = models.FloatField('Time gained to listen an advertisement (s)', default=3)
    minimum_reports_ban = models.PositiveIntegerField('Minimum reports to ban an audio', default=10)
    time_extend_audio = models.PositiveIntegerField('Extend audio with like (s)', default=3600)

    class Meta:
        db_table = 'configuration'
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configuration'

    def __str__(self):
        return "SoundGo configuration"
