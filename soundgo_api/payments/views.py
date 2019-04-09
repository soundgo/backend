
import stripe
from django.conf import settings
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from datetime import datetime, date
from accounts.views import login
from accounts.models import Actor
from records.models import Advertisement, Reproduction

stripe.api_key = settings.STRIPE_SECRET_KEY


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@transaction.atomic
def charge(request, actor_id):

    response_data_save = {"error": "SAVE_CHARGE", "details": "There was an error to save the charge"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_data_amount = {"error": "NOT_AMOUNT", "details": "Amount must be greater than 50"}

    if request.method == 'POST':
        try:

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
                return JSONResponse(charge, status=200)
            else:
                return JSONResponse(response_data_amount, status=400)
        except Exception or ValueError or KeyError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)
