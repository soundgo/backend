from django.shortcuts import render

# Create your views here.
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
import rest_framework
from django.contrib.auth.models import AnonymousUser
from .models import UserAccount, Actor
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer




class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def login(request, role):

    request.user = AnonymousUser()

    response_not_token = {"error": "TOKEN_NOT_FOUND", "details": "You must specify the token"}
    response_not_valid = {"error": "TOKEN_NOT_VALID", "details": "The token is not valid"}
    actor_not_allowed = {"error": "ACTOR_NOT_ALLOWED", "details": "The actor can not do this action"}


    if request.META.get('HTTP_AUTHORIZATION') == None or request.META.get('HTTP_AUTHORIZATION').strip() == "":
        return JSONResponse(response_not_token, status=400)

    else:
        data = {'token': request.META.get('HTTP_AUTHORIZATION').split()[1]}

        try:
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            request.user= UserAccount.objects.filter(nickname=valid_data['user']).all()[0]

            if role == "admin":
                # Verificar que es un admin
                if not request.user.admin:
                    return JSONResponse(actor_not_allowed, status=400)

            elif role == "advertiser":
                actor= Actor.objects.filter(user_account= request.user).all()[0]
                if actor.credit_card == None:
                    return JSONResponse(actor_not_allowed, status=400)

            elif role == "user":
                #Verificar q no tenga tarjeta y no sea admin
                actor = Actor.objects.filter(user_account=request.user).all()[0]
                if actor.credit_card != None or request.user.admin:
                    return JSONResponse(actor_not_allowed, status=400)

            elif role == "all":
                pass

            else:
                raise Exception("Role not found")

        except rest_framework.exceptions.ValidationError as error:
            request.user = AnonymousUser()
            return JSONResponse(response_not_valid, status=400)



def logout(request):
    request.user = AnonymousUser()
