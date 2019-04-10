from apscheduler.schedulers.blocking import BlockingScheduler

from records.models import Audio, Advertisement
from accounts.models import Actor, CreditCard
from sites.models import Site

from managers.payment_manager import charge

import datetime

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', id='charge_advertisements_job_id', day='last', hour=0)
def charge_advertisements_job():

    """
    CRON job to charge the advertisements.
    TRIGGER: Last day of each month at 0 AM.
    """

    advertisers = Actor.objects.filter(credit_card__isnull=False)

    for advertiser in advertisers:

        charge(advertiser.id)


@scheduler.scheduled_job('cron', id='delete_marked_advertisements_job_id', day='last', hour=1)
def delete_marked_advertisements_job():

    """
    CRON job to delete the advertisements marked for deletion.
    TRIGGER: Last day of each month at 1 AM.
    """

    Advertisement.objects.filter(isDelete=True).delete()


@scheduler.scheduled_job('cron', id='delete_marked_credit_card_job_id', day='last', hour=2)
def delete_marked_credit_card_job():

    """
    CRON job to delete the credit cards marked for deletion.
    TRIGGER: Last day of each month at 2 AM.
    """

    credit_cards = CreditCard.objects.filter(isDelete=True)

    for credit_card in credit_cards:

        Site.objects.filter(actor__credit_card=credit_card).delete()
        Advertisement.objects.filter(actor__credit_card=credit_card).delete()

        credit_card.delete()


@scheduler.scheduled_job('cron', id='reactivate_inactive_advertisements_job_id', day='last', hour=3)
def reactivate_inactive_advertisements_job():

    """
    CRON job to reactivate the inactive advertisements.
    TRIGGER: Last day of each month at 3 AM.
    """

    Advertisement.objects.filter(isActive=False).update(isActive=True)


@scheduler.scheduled_job('cron', id='delete_past_audios_job_id', day_of_week='wed', hour=5)
def delete_past_audios_job():

    """
    CRON job to delete past audios.
    TRIGGER: Each wednesday of each week of each month at 5 AM.
    """

    Audio.objects.filter(timestampFinish__lt=datetime.datetime.now()).delete()


scheduler.start()
