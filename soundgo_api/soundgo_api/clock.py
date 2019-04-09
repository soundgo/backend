from apscheduler.schedulers.blocking import BlockingScheduler

from records.models import Advertisement
from accounts.models import CreditCard
from sites.models import Site

scheduler = BlockingScheduler()


# TODO: Add CRON job for payment


@scheduler.scheduled_job('cron', id='delete_marked_advertisements_job_id', day='last', hour=1)
def delete_marked_advertisements_job():

    """
    CRON job to delete the advertisements marked for deletion.
    """

    Advertisement.objects.filter(isDelete=True).delete()


@scheduler.scheduled_job('cron', id='delete_marked_credit_card_job_id', day='last', hour=2)
def delete_marked_credit_card_job():

    """
    CRON job to delete the credit cards marked for deletion.
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
    """

    Advertisement.objects.filter(isActive=False).update(isActive=True)


scheduler.start()
