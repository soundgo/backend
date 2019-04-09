
import stripe
from django.conf import settings
from datetime import datetime, date
from accounts.models import Actor
from records.models import Advertisement, Reproduction

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge(actor_id):

    creditcard = Actor.objects.get(pk=actor_id).credit_card
    amount = 0
    advertisements = Advertisement.objects.filter(actor=actor_id)
    today = date.today()
    for ad in advertisements:
        reproductions = len(Reproduction.objects.filter(advertisement=ad.id).filter(date__month=today.month,
                                                                                    date__year=today.year))
        amount = amount + (reproductions * ad.duration * ad.radius/10000)

        if amount >= 50:
            customer = stripe.Customer.create(
                description=str(Actor.objects.get(pk=actor_id).email),
                # source='tok_es'
                source = {
                    "object": "card",
                    "name": creditcard.brandName,
                    "brand": creditcard.brandName,
                    "country": "ES",
                    "cardholder": creditcard.holderName,
                    "cvc_check": creditcard.cvvCode,
                    "exp_month": creditcard.expirationMonth,
                    "exp_year": creditcard.expirationYear,
                        "number":  4000007240000007, # creditcard.number,
                        "funding": "credit",
                        "metadata": {},
                    }
                )
            customer = customer.save()

            charge = stripe.Charge.create(
                amount = amount,
                currency = 'eur',
                description = 'SoundGo advertising ' + str(datetime.now().month) + "/" + str(datetime.now().year),
                customer = customer,
            )
            charge.save()

            return charge
