
import stripe
from django.conf import settings
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from accounts.views import login
from accounts.models import Actor

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
def charge(request):

    response_data_save = {"error": "SAVE_CHARGE", "details": "There was an error to save the charge"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    if request.method == 'POST':
        try:

            login(request, 'advertiser')
            creditcard = Actor.objects.get(user_account=request.user.id).credit_card
            print(creditcard)

            charge = stripe.Charge.create(
                amount = 500,
                currency = 'eur',
                description = 'SoundGo advertising ' + str(datetime.now().month) + "/" + str(datetime.now().year),
                # customer = str(request.user.nickname),
                source = 'tok_es'
                # source = {
                #     "object": "card",
                #     "brand": creditcard.brandName,
                #     "country": "ES",
                #     "cardholder": creditcard.holderName,
                #     "cvc_check": creditcard.cvvCode,
                #     "exp_month": creditcard.expirationMonth,
                #     "exp_year": creditcard.expirationYear,
                #     "number": creditcard.number,
                #     "funding": "credit",
                #     "metadata": {},
                # }
            )
            charge.save()
            return JSONResponse(charge, status=200)
        except Exception or ValueError or KeyError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)
