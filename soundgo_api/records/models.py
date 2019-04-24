from django.db import models

from accounts.models import Actor
from sites.models import Site
from tags.models import Tag

from django.dispatch import receiver
from django.db.models.signals import post_delete

from managers.firebase_manager import remove_audio, remove_advertisement
from managers.cloudinary_manager import remove_record

# ################################################## #
# ##############        MODELS        ############## #
# ################################################## #


class Record(models.Model):
    actor = models.ForeignKey(Actor, null=False, on_delete=models.CASCADE, related_name='records')

    latitude = models.FloatField()
    longitude = models.FloatField()
    numberReproductions = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    path = models.CharField(blank=False, max_length=800)


class Audio(Record):
    site = models.ForeignKey(Site, null=True, blank=True, related_name='records', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    isInappropriate = models.BooleanField(verbose_name='Inappropriate', default=False)
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


class Report(models.Model):
    actor = models.ForeignKey(Actor, null=False, on_delete=models.CASCADE, related_name='reports')
    audio = models.ForeignKey(Audio, null=False, on_delete=models.CASCADE, related_name='reports')

    class Meta:
        db_table = 'report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        unique_together = ('actor', 'audio',)

    def __str__(self):
        return "Report"


class Reproduction(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="reproductions")
    date = models.DateTimeField(auto_now_add=True, editable=False)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="reproductions")

    class Meta:
        db_table = 'reproduction'
        verbose_name = 'Reproduction'
        verbose_name_plural = 'Reproductions'

    def __str__(self):
        return 'Reproduction'


# ################################################## #
# #############        SIGNALS        ############## #
# ################################################## #

@receiver(post_delete, sender=Audio)
def auto_delete_audio_on_third_party_services(sender, instance, **kwargs):

    """
    Signal to delete the audio from Cloudinary and Firebase after PostgreSQL deletion.
    """

    # Delete from Firebase
    remove_audio(instance)

    # Delete from Cloudinary
    remove_record(instance.path)


@receiver(post_delete, sender=Advertisement)
def auto_delete_advertisement_on_third_party_services(sender, instance, **kwargs):

    """
    Signal to delete the advertisement from Cloudinary and Firebase after PostgreSQL deletion.
    """

    # Delete from Firebase
    remove_advertisement(instance)

    # Delete from Cloudinary
    remove_record(instance.path)

