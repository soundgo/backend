from django.shortcuts import render

# Create your views here.
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
import rest_framework
from django.contrib.auth.models import AnonymousUser
from .models import UserAccount, Actor, CreditCard
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from .serializers import ActorSerializer, CreditCardSerializer
from rest_framework_jwt.views import obtain_jwt_token
from django.db import transaction
from rest_framework.parsers import JSONParser
from django.contrib.auth import  get_user_model
from django.core.validators import validate_email
from managers.cloudinary_manager import upload_photo, remove_photo



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

        try:
            data = {'token': request.META.get('HTTP_AUTHORIZATION').split()[1]}
        except Exception as e:
            return JSONResponse({"error": "TOKEN_NOT_FOUND", "details": str(e)}, status=400)

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

            data = {}

            jwt = obtain_jwt_token(request)
            if jwt.status_code != 200:
                return JSONResponse(jwt.data, status=400)

            valid_data = VerifyJSONWebTokenSerializer().validate({'token':jwt.data['token']})
            actor = Actor.objects.filter(user_account__nickname=valid_data['user']).all()[0]


            data["token"] = jwt.data['token']

            if actor.user_account.is_admin:
                data["role"] = "admin"
            elif actor.credit_card == None:
                data["role"] = "user"
            else:
                data["role"] = "advertiser"

            data["actorId"] =  actor.id

            return JSONResponse(data, status=200)

        except Exception or KeyError or ValueError as e:
            response_not_valid["details"] = str(e)
            return JSONResponse(response_not_valid, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)




@csrf_exempt
@transaction.atomic
def actor_get_update(request, nickname):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_actor_not_found = {"error": "ACTOR_NOT_FOUND", "details": "The actor does not exit"}
    response_actor_get = {"error": "ACTOR_GET", "details": "The actor does not exit"}
    response_data_update = {"error": "UPDATE_ACTOR", "details": "There was an error to save the actor"}

    login_result = login(request, 'advertiserUser')
    if login_result is not True:
        return login_result

    try:

        actor = Actor.objects.filter(user_account__nickname= nickname).all()[0]
    except Exception:
        return JSONResponse(response_actor_not_found, status=404)

    if request.user.id != actor.user_account.id:
        response_data_update = {"error": "ACTOR_NOT_ALLOWED", "details": "This actor can not edit or view this profile"}

    if request.method == 'GET':

        try:

            serializer = ActorSerializer(actor)
            data_aux = serializer.data
            data_aux["nickname"] = actor.user_account.nickname

        except Exception or ValueError or KeyError as e:
            response_actor_get["details"] = str(e)
            return JSONResponse(response_actor_get, status= 400)

        return JSONResponse(data_aux)

    elif request.method == 'PUT':
        lastPhoto= None
        try:
            with transaction.atomic():

                data = JSONParser().parse(request)

                userAccount = UserAccount.objects.filter(nickname=nickname).all()[0]

                # Check password
                if data.get('password') != None:

                    if data.get('password').strip() != "":
                        userAccount.set_password(data.get('password'))
                    else:
                        return JSONResponse({"error": "UPDATE_ACTOR",
                                             "details": "You must write a password"},
                                            status=400)

                # Check nickname
                if data.get('nickname') != None:
                    if len(UserAccount.objects.filter(
                            nickname=data.get('nickname')).all()) != 0 and actor.user_account.nickname != data.get('nickname'):
                        return JSONResponse({"error": "UPDATE_ACTOR",
                                             "details": "This nickname is been using by another actor."},
                                            status=400)

                    elif data.get('nickname').strip() != "":
                        userAccount.nickname = data.get('nickname')

                    else:
                        return JSONResponse({"error": "UPDATE_ACTOR",
                                             "details": "You must write a nickname"},
                                            status=400)

                # Check email
                if data.get('email') != None:
                    if len(Actor.objects.filter(email=data.get('email')).all()) != 0 and actor.email != data.get(
                            'email'):

                        return JSONResponse({"error": "EMAIL_USED",
                                             "details": "This email is been using by another actor."},
                                            status=400)
                    else:

                        try:
                            validate_email(data.get('email'))
                            actor.email= data.get('email')
                        except Exception:

                            return JSONResponse({"error": "EMAIL_NOT_VALID",
                                                 "details": "This email is not valid."},
                                                status=400)


                # check photo
                changePhoto = False
                if data.get('base64') != None:
                    savePhoto = upload_photo(data.get('base64'))

                    if savePhoto == "":
                        raise Exception("There base64 of photo is not correct.")

                    lastPhoto = actor.photo
                    changePhoto = True
                    actor.photo = savePhoto


                #Save data
                actor.save()
                userAccount.save()

                #Delete the old photo
                if lastPhoto != None and lastPhoto != "" and changePhoto:
                    removePhoto = remove_photo(lastPhoto)

                    if removePhoto == False:
                        raise Exception("There was a problem when try to remove last photo")


                serializer = ActorSerializer(actor)

                data = serializer.data


                return JSONResponse(data)



        except Exception or ValueError or KeyError as e:

            response_data_update["details"] = str(e)
            return JSONResponse(response_data_update, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)

@csrf_exempt
@transaction.atomic
def actor_create(request):

    response_data_save = {"error": "SAVE_REPORT", "details": "There was an error to save the actor"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    if request.method == 'POST':

        try:
            data = JSONParser().parse(request)
            data_actor = {}

            UserAccount = get_user_model()
            user_account = UserAccount.objects.create_user_account(data["nickname"], data["password"])

            data_actor['user_account'] = user_account.id
            if 'base64' in data:
                data_actor['photo'] =  upload_photo(data['base64'])
            else:
                data_actor['photo'] = ""
            data_actor['email'] = data['email']
            data_actor["minutes"] = 300

            serializer = ActorSerializer(data=data_actor)

            if serializer.is_valid():
                # Save in db
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            response_data_save["details"] = serializer.errors
            if 'base64' in data:
                remove_photo(data_actor['photo'])
            user_account.delete()
            return JSONResponse(response_data_save, status=400)

        except Exception or ValueError or KeyError as e:
            response_data_save["details"] = str(e)
            if 'base64' in data and 'photo' in data_actor:
                remove_photo(data_actor['photo'])
                try:
                    if user_account:
                        user_account.delete()
                except Exception:
                    pass
                return JSONResponse(response_data_save, status=400)
            else:
                try:
                    if user_account:
                        user_account.delete()
                except Exception:
                    pass
                return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)

@csrf_exempt
@transaction.atomic
def creditcard_create(request):

    response_data_save = {"error": "SAVE_CREDITCARD", "details": "There was an error to save the credit card"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    if request.method == 'POST':

        login_result = login(request, 'user')
        if login_result is not True:
            return login_result

        try:

            data = JSONParser().parse(request)

            data = pruned_serializer_credit_card_create(data)
            serializer = CreditCardSerializer(data=data)
            if serializer.is_valid():
                # Save in db
                credit_card = serializer.save()
                actor = Actor.objects.get(user_account=request.user.id)
                actor.credit_card = credit_card
                actor.save()
                return JSONResponse(serializer.data, status=201)
            response_data_save["details"] = serializer.errors
            return JSONResponse(response_data_save, status=400)

        except Exception or ValueError or KeyError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
@transaction.atomic
def creditcard_update_get(request, creditcard_id):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_creditcard_not_found = {"error": "CREDITCARD_NOT_FOUND", "details": "The credit card does not exit"}
    response_creditcard_not_see = {"error": "CREDITCARD_NOT_SEE", "details": "You cannot se this creditcard"}
    response_creditcard_put = {"error": "PUT_CREDITCARD", "details": "There was an error to update the creditcard"}
    response_creditcard_not_put = {"error": "NOT_PUT_CREDITCARD", "details": "You can not update the credit card"}
    response_creditcard_get = {"error": "NOT_GET_CREDITCARD", "details": "You can not update the credit card"}

    try:
        credit_card = CreditCard.objects.get(pk=creditcard_id)
    except CreditCard.DoesNotExist:
        return JSONResponse(response_creditcard_not_found, status=404)
    actor = Actor.objects.get(credit_card=credit_card.id)

    if request.method == 'GET':

        login_result = login(request, 'advertiser')
        login_result2 = login(request, 'admin')
        if login_result is not True and login_result2 is not True:
            return login_result

        if login_result is True:
            actor_aux = Actor.objects.get(user_account=request.user.id)
            if actor_aux.credit_card.id != credit_card.id:
                return JSONResponse(response_creditcard_not_see, status=400)

        try:

            serializer = CreditCardSerializer(credit_card)
            data_aux = serializer.data
            data_aux["name"] = actor.user_account.nickname
            data_aux["photo"] = actor.photo

        except Exception or ValueError or KeyError as e:
            response_creditcard_get["details"] = str(e)
            return JSONResponse(response_creditcard_get, status=400)

        return JSONResponse(data_aux, status=200)

    elif request.method == 'PUT':

        login_result = login(request, 'advertiser')
        if login_result is not True:
            return login_result

        if request.user.id != actor.user_account.id:
            return JSONResponse(response_creditcard_not_put, status=200)
        try:
            data = JSONParser().parse(request)

            serializer = CreditCardSerializer(credit_card, data=data)

            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=200)
            response_creditcard_put["details"] = serializer.errors
            return JSONResponse(response_creditcard_put, status=400)

        except Exception or ValueError or KeyError as e:
            response_creditcard_put["details"] = str(e)
            return JSONResponse(response_creditcard_put, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


def pruned_serializer_credit_card_create(data):
    data['isDelete'] = False
    return data
