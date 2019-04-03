from django.db import models

from accounts.models import Actor
from sites.models import Site
from tags.models import Tag


class Record(models.Model):
    actor = models.ForeignKey(Actor, null=False, on_delete=models.CASCADE, related_name='records')

    latitude = models.FloatField()
    longitude = models.FloatField()
    numberReproductions = models.IntegerField(default=0)
    path = models.CharField(blank=False, max_length=800)


class Audio(Record):
    site = models.ForeignKey(Site, null=True, blank=True, related_name='records', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    isInappropriate = models.BooleanField(default=False)
    timestampCreation = models.DateTimeField(auto_now_add=True, editable=False)
    timestampFinish = models.DateTimeField()

    class Meta:
        db_table = 'audio'
        verbose_name = 'Audio'
        verbose_name_plural = 'Audios'


class Advertisement(Record):
    maxPriceToPay = models.FloatField()
    radius = models.IntegerField()
    isActive = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertisement'
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


class Category(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    maxTimeRecord = models.FloatField(default=60)
    minDurationMap = models.FloatField(default=259200)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return "%s" % self.name


class Like(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor")

    class Meta:
        db_table = 'like'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('actor', 'audio')

    def __str__(self):
        return 'Like'

