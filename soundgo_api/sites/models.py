from django.db import models
from accounts.models import Actor

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from managers.firebase_manager import add_site, update_site, remove_site

# ################################################## #
# ##############        MODELS        ############## #
# ################################################## #


class Site(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(blank=False, max_length=200)
    description = models.CharField(blank=False, max_length=200)
    actor = models.ForeignKey(Actor, null=False, on_delete=models.CASCADE, related_name='sites')

    class Meta:
        db_table = 'site'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


# ################################################## #
# #############        SIGNALS        ############## #
# ################################################## #

@receiver(post_save, sender=Site)
def auto_create_update_site_in_third_party_services(sender, instance, created, **kwargs):

    """
    Signal to create/update the site in Firebase after PostgreSQL insertion.
    """

    if created:

        # Create the site in Firebase
        add_site(instance)

    else:

        # Update the site in Firebase
        update_site(instance)


@receiver(post_delete, sender=Site)
def auto_delete_site_on_third_party_services(sender, instance, **kwargs):

    """
    Signal to delete the site from Firebase after PostgreSQL deletion.
    """

    # Delete from Firebase
    remove_site(instance)
