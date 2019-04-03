from django.shortcuts import render

# Create your views here.
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
import rest_framework
from django.contrib.auth.models import AnonymousUser
from .models import UserAccount, Actor
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from .serializers import ActorSerializer
from rest_framework_jwt.views import obtain_jwt_token



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

    print(request.META.get('HTTP_AUTHORIZATION'))
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
                if actor.credit_card == None or request.user.admin: #Segunda condicion nueva
                    return JSONResponse(actor_not_allowed, status=400)

            elif role == "user":
                #Verificar q no tenga tarjeta y no sea admin
                actor = Actor.objects.filter(user_account=request.user).all()[0]
                if actor.credit_card != None or request.user.admin:
                    return JSONResponse(actor_not_allowed, status=400)

            elif role == "advertiserUser":
                if request.user.admin:
                    return JSONResponse(actor_not_allowed, status=400)

            elif role == "all":
                pass

            else:
                raise Exception("Role not found")

        except rest_framework.exceptions.ValidationError as error:
            request.user = AnonymousUser()
            return JSONResponse(response_not_valid, status=400)

    return True



def logout(request):
    request.user = AnonymousUser()



@csrf_exempt
def get_token(request):
    response_not_valid = {"error": "AUTHENTICATION_NOT_VALID", "details": "The authentication is not valid"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}


    if request.method == 'POST':

        try:


            data={}

            jwt= obtain_jwt_token(request)
            if jwt.status_code != 200:
                return JSONResponse(jwt.data, status=400)

            valid_data = VerifyJSONWebTokenSerializer().validate({'token':jwt.data['token']})
            actor = Actor.objects.filter(user_account__nickname=valid_data['user']).all()[0]

            print(actor)
            data["token"]=  jwt.data['token']


            if actor.user_account.is_admin:
                data["role"] = "admin"
            elif actor.credit_card == None:
                data["role"] = "user"
            else:
                data["role"] = "advertiser"

            data["actorId"] =  actor.id

            return JSONResponse(data, status=200)



        except Exception  or KeyError or ValueError as e:
            return JSONResponse(response_not_valid, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
def actor_get(request, nickname):


    response_data_get = {"error": "GET_ACTOR", "details": "There was an error to "
                                                                     "get the actor"}

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_actor_not_found = {"error": "ACTOR_NOT_FOUND",
                                        "details": "The actor does not exit"}

    try:

        actor = Actor.objects.filter(user_account__nickname= nickname).all()[0]
    except Exception:
        return JSONResponse(response_actor_not_found, status=404)

    if request.method == 'GET':

        try:

            serializer = ActorSerializer(actor)

        except Exception or ValueError or KeyError:
            return JSONResponse(response_data_get, status= 400)


        return JSONResponse(serializer.data)
    else:
        return JSONResponse(response_data_not_method, status=400)
