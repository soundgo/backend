from apscheduler.schedulers.blocking import BlockingScheduler

from records.models import Advertisement
from accounts.models import CreditCard

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

    CreditCard.objects.filter(isDelete=True).delete()


scheduler.start()