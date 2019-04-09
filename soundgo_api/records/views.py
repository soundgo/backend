from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Advertisement, Audio, Category, Like, Report, Reproduction
from sites.models import Site
from .serializers import (AdvertisementSerializer, AudioSerializer, LikeSerializer,
                          ReportSerializer, ReproductionSerializer)
from datetime import datetime, date
from django.db import transaction
from managers.cloudinary_manager import upload_record, remove_record, get_record_duration
from accounts.models import Actor
from accounts.views import login
from managers.firebase_manager import (add_audio, update_audio, add_advertisement,
                                       update_advertisement, remove_advertisement)
from configuration.models import Configuration
from datetime import timedelta
from tags.models import Tag


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
def advertisement_create(request):
    response_data_save = {"error": "SAVE_ADVERTISEMENT", "details": "There was an error to save the advertisement"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_audio_not_belong = {"error": "AUDIO_NOT_BELONG", "details": "Audio creator is not logged user"}
    response_actor_not_credit_card = {"error": "ACTOR_NOT_CREDIT_CARD", "details": "Logged user does not have a credit card"}
    response_price_negative = {"error": "MAX_PRICE_NEGATIVE", "details": "The max price can not be negative"}
    response_radius_negative = {"error": "RADIUS_NEGATIVE", "details": "The radius is not in the valid range"}

    if request.method == 'POST':

        try:
            with transaction.atomic():

                data = JSONParser().parse(request)

                # Comprobar que es anunciante
                login_result = login(request, 'advertiser')

                if login_result is not True:
                    return login_result

                # Comprobar que que tiene tarjeta de credito
                if login_result is True:
                    actor_aux = Actor.objects.get(user_account=request.user.id)
                    if actor_aux.credit_card is None:
                        return JSONResponse(response_actor_not_credit_card, status=400)

                actor = Actor.objects.get(user_account=request.user.id)
                data['actor'] = actor.id

                # coger el base 64 y guardar , meter en data['path'] la url que retorne
                try:
                    data['path'] = upload_record(data['base64'])
                    data = pruned_serializer_advertisement_create(data)
                    configuration = Configuration.objects.all()[0]

                    if (type(data["maxPriceToPay"]) is float or type(data["maxPriceToPay"]) is int) and \
                            data["maxPriceToPay"] <= 0:
                        remove_record(data['path'])
                        return JSONResponse(response_price_negative, status=400)

                    if type(data["radius"]) is int and (
                            data["radius"] < configuration.minimum_radius or data["radius"] > configuration.maximum_radius):
                        remove_record(data['path'])
                        return JSONResponse(response_radius_negative, status=400)

                    serializer = AdvertisementSerializer(data=data)
                except Exception:
                    if 'path' in data:
                        remove_record(data['path'])
                        return JSONResponse(response_data_save, status=400)
                    else:
                        return JSONResponse(response_data_save, status=400)

                if serializer.is_valid():
                    # Save in db
                    advertisement = serializer.save()
                    # Save in Firebase Cloud Firestore
                    add_advertisement(advertisement)
                    return JSONResponse(serializer.data, status=201)
                remove_record(data['path'])
                response_data_save["details"] = serializer.errors
                return JSONResponse(response_data_save, status=400)

        except Exception or KeyError or ValueError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(str(e), status=400)

    else:
        return JSONResponse(response_data_not_method,
                            status=400)


@csrf_exempt
@transaction.atomic
def advertisement_update_get(request, advertisement_id):

    response_data_put = {"error": "UPDATE_ADVERTISEMENT", "details": "There was an error to "                                                                                                                                                 
                                                                     "update the advertisement"}

    response_data_get = {"error": "GET_ADVERTISEMENT", "details": "There was an error to "
                                                                     "get the advertisement"}

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_advertisement_not_found = {"error": "ADVERTISEMENT_NOT_FOUND",
                                        "details": "The advertisement does not exit"}
    response_data_deleted = {"error": "DELETE_ADVERTISEMENT", "details": "The advertisement is deleted"}
    response_audio_not_belong = {"error": "AUDIO_NOT_BELONG", "details": "Audio creator is not logged user"}
    response_price_negative = {"error": "MAX_PRICE_NEGATIVE", "details": "The max price can not be negative"}

    try:
        advertisement = Advertisement.objects.get(pk=advertisement_id)
    except Advertisement.DoesNotExist:
        return JSONResponse(response_advertisement_not_found, status=404)

    if request.method == 'GET':

        try:

            serializer = AdvertisementSerializer(advertisement)

        except Exception or ValueError or KeyError as e:
            response_data_get["details"] = str(e)
            return JSONResponse(response_data_get, status= 400)

        data_aux = serializer.data
        data_aux.pop('actor')
        data_aux["name"] = advertisement.actor.user_account.nickname
        data_aux["photo"] = advertisement.actor.photo
        return JSONResponse(data_aux, status=200)

    elif request.method == 'PUT':

        try:
            with transaction.atomic():

                login_result = login(request, 'advertiser')
                if login_result is not True:
                    return login_result

                # Comprobar que el creador del audio es el usuario autenticado
                if login_result is True:
                    actor_aux = Actor.objects.get(user_account=request.user.id)
                    if actor_aux.id != advertisement.actor.id:
                        return JSONResponse(response_audio_not_belong, status=400)

                if advertisement.isDelete is True:
                    return JSONResponse(response_data_deleted, status=400)

                data = JSONParser().parse(request)

                data = pruned_serializer_advertisement_update(advertisement, data)
                if (type(data["maxPriceToPay"]) is float or type(data["maxPriceToPay"]) is int) and data["maxPriceToPay"] <= 0:
                    return JSONResponse(response_price_negative, status=400)
                serializer = AdvertisementSerializer(advertisement, data=data)
                if serializer.is_valid():
                    ad = serializer.save()

                    # Si lo quiere borrar se va a marcar como borrado y se borra de mapbox y del servidor
                    if data['isDelete']:
                        # Borrar grabacion de servidor
                        result = remove_record(advertisement.path)
                        if not result:
                            return JSONResponse(response_data_put, status=400)
                        # Remove advertisement from Firebase Cloud Firestore
                        remove_advertisement(advertisement)

                    # Update in Firebase
                    update_advertisement(ad)

                    return JSONResponse(serializer.data)
                response_data_put["details"] = serializer.errors
                return JSONResponse(response_data_put, status=400)

        except Exception or ValueError or KeyError as e:
            response_data_put["details"] = str(e)
            return JSONResponse(response_data_put, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)


# Metodos audios
@csrf_exempt
@transaction.atomic
def audio_create(request):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_data_save = {"error": "SAVE_AUDIO", "details": "There was an error to save the audio"}
    response_data_not_minutes = {"error": "NOT_MINUTES", "details": "You do not have enough time to record this audio"}
    response_data_incorrect_base64 = {"error": "AUDIO_INCORRECT_BASE64", "details": "Invalid base64"}

    if request.method == 'POST':

        try:
            with transaction.atomic():

                data = JSONParser().parse(request)

                login_result = login(request, 'advertiserUser')
                if login_result is not True:
                    return login_result

                # El creador del audio es el usuario autenticado

                actor = Actor.objects.get(user_account=request.user.id)
                data['actor'] = actor.id
                # Fin user de prueba

                # Coger el base 64 y guardar , meter en data['path'] la url que retorne
                try:
                    data['path'] = upload_record(data['base64'])

                    if data['path'] == '':
                        return JSONResponse(response_data_incorrect_base64, status=400)

                    data = pruned_serializer_audio_create(data)
                    serializer = AudioSerializer(data=data)
                except Exception:
                    if 'path' in data:
                        remove_record(data['path'])
                        return JSONResponse(response_data_save, status=400)
                    else:
                        return JSONResponse(response_data_save, status=400)

                # Ver si cumple los tiempos
                duration = data['duration']
                if actor.minutes < duration:
                    remove_record(data['path'])
                    return JSONResponse(response_data_not_minutes, status=400)
                else:
                    actor.minutes = actor.minutes - duration

                if serializer.is_valid():
                    # Save in db
                    audio = serializer.save()
                    # Save in Firebase Cloud Firestore
                    add_audio(audio)
                    # Save actor with new minutes
                    actor.save()
                    data_aux = serializer.data
                    data_aux["category"] = audio.category.name
                    return JSONResponse(data_aux, status=201)
                remove_record(data['path'])
                response_data_save["details"] = serializer.errors
                return JSONResponse(response_data_save, status=400)

        except Exception or KeyError or ValueError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
@transaction.atomic
def audio_delete_get_update(request, audio_id):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_audio_not_found = {"error": "AUDIO_NOT_FOUND", "details": "The audio does not exit"}
    response_audio_get = {"error": "GET_AUDIO", "details": "There was an error to get the audio"}
    response_audio_delete = {"error": "DELETE_AUDIO", "details": "There was an error to delete the audio"}
    response_audio_not_belong = {"error": "AUDIO_NOT_BELONG", "details": "Audio creator is not logged user"}
    category_not_found = {"error": "CATEGORY_NOT_FOUND", "details": "The category doesn't exists"}
    category_bad_request = {"error": "GET_CATEGORY", "details": "You must specify the category"}
    tags_bad_request = {"error": "GET_TAGS", "details": "You must specify the tags"}

    try:
        audio = Audio.objects.get(pk=audio_id)
    except Audio.DoesNotExist:
        return JSONResponse(response_audio_not_found, status=404)

    if request.method == 'GET':

        try:

            login_result = login(request, 'advertiserUser')
            serializer = AudioSerializer(audio)
            data_aux = serializer.data
            data_aux["category"] = audio.category.name
            data_aux.pop("actor")
            data_aux["name"] = audio.actor.user_account.nickname
            data_aux["photo"] = audio.actor.photo
            data_aux["numberLikes"] = len(Like.objects.filter(audio=audio_id))
            data_aux["liked"] = False

            if login_result is True and len(Like.objects.filter(audio=audio_id).filter(actor__user_account=request.user.id)) != 0:
                data_aux["liked"] = True

            data_aux["reported"] = False

            if login_result is True:
                report = Report.objects.filter(audio=audio.id).filter(actor__user_account=request.user.id)
                if report:
                    data_aux["reported"] = True

            # Return tags name
            tagsNames = []
            for tagId in serializer.data['tags']:
                tag = Tag.objects.filter(pk=tagId).all()[0]
                tagsNames.append(tag.name)

            data_aux.pop("tags")
            data_aux['tags'] = tagsNames

        except Exception or ValueError or KeyError as e:
            response_audio_get["details"] = str(e)
            return JSONResponse(response_audio_get, status=400)

        return JSONResponse(data_aux, status=200)

    elif request.method == 'DELETE':

        try:
            with transaction.atomic():
                # Comprobar que solo lo puede borrar el creador del audio o un administrador
                login_result = login(request, 'advertiserUser')
                login_result2 = login(request, 'admin')
                if login_result is not True and login_result2 is not True:
                    return login_result

                if login_result is True:
                    actor_aux = Actor.objects.get(user_account=request.user.id)
                    if actor_aux.id != audio.actor.id:
                        return JSONResponse(response_audio_not_belong, status=400)

                audio.delete()

        except Exception or KeyError or ValueError as e:
            response_audio_delete["details"] = str(e)
            return JSONResponse(response_audio_delete, status=400)

        return HttpResponse(status=204)

    elif request.method == 'PUT':

        login_result = login(request, 'advertiserUser')
        if login_result is not True:
            return login_result

        # Is the user or advertiser of the audio
        if not audio.actor.user_account.id == request.user.id:
            return JSONResponse({"error": "ACTOR_NOT_ALLOW",
                                 "details": "This actor can not edit the audio"}, status=404)

        try:

            with transaction.atomic():
                data = JSONParser().parse(request)

                # Check category
                if data.get('category') != None:
                    category = Category.objects.filter(name=data.get('category')).all()

                    if len(category) == 0:
                        return JSONResponse(category_not_found, status=404)
                    else:
                        audio.category = category[0]
                else:
                    return JSONResponse(category_bad_request, status=400)

                # Check tags
                if data.get('tags') == None:
                    return JSONResponse(tags_bad_request, status=404)

                # Update tags
                audioTags = [tag.name for tag in audio.tags.all()]
                tagsNameCheck = set(data.get('tags')) ^ set(audioTags)

                for tagName in tagsNameCheck:
                    tag = Tag.objects.filter(name=tagName).all()

                    if len(tag) == 0:
                        tag = Tag.objects.create(name=tagName)
                        audio.tags.add(tag)
                    elif tag[0].name in audioTags:
                        audio.tags.remove(tag[0])

                        # If the tag never used delete of the system
                        audios = Audio.objects.all().filter(tags__name=tag[0].name).all()

                        if len(audios) == 0:
                            tag[0].delete()

                    else:
                        audio.tags.add(tag[0])

                audio.save()

                serializer = AudioSerializer(audio)

                # Return tags name
                tagsNames = []
                for tagId in serializer.data['tags']:
                    tag = Tag.objects.filter(pk=tagId).all()[0]
                    tagsNames.append(tag.name)

                data = serializer.data
                data.pop("tags")
                data['tags'] = tagsNames

                update_audio(audio, tagsNames)

                return JSONResponse(data)

        except Exception or ValueError or KeyError as e:
            return JSONResponse({"error": "UPDATE_AUDIO", "details": str(e)}, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


# Metodo site
@csrf_exempt
@transaction.atomic
def audio_site_create(request, site_id):
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}
    response_data_save = {"error": "SAVE_AUDIO", "details": "There was an error to save the audio"}
    response_data_not_minutes = {"error": "NOT_MINUTES", "details": "You do not have enough time to record this audio"}
    response_audio_not_belong = {"error": "AUDIO_NOT_BELONG", "details": "Audio creator is not logged user"}

    try:
        Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'POST':

        login_result = login(request, 'advertiserUser')
        if login_result is not True:
            return login_result

        try:
            with transaction.atomic():

                data = JSONParser().parse(request)

                # Comprobar que el creador del audio es el usuario autenticado
                actor = Actor.objects.get(user_account=request.user.id)
                data['actor'] = actor.id
                # Fin user de prueba
                try:
                    data = pruned_serializer_audio_create_site(data, site_id)
                    # Metemos en el audio el site
                    data['site'] = site_id
                    serializer = AudioSerializer(data=data)

                    # Coger el base 64 y guardar , meter en data['path'] la url que retorne
                    data['path'] = upload_record(data['base64'])
                except Exception:
                    if 'path' in data:
                        remove_record(data['path'])
                        return JSONResponse(response_data_save, status=400)
                    else:
                        return JSONResponse(response_data_save, status=400)

                # Ver si cumple los tiempos
                duration = get_record_duration(data['path'])
                if actor.minutes < duration:
                    remove_record(data['path'])
                    return JSONResponse(response_data_not_minutes, status=400)
                else:
                    actor.minutes = actor.minutes - duration

                if serializer.is_valid():
                    audio = serializer.save()
                    actor.save()
                    data_aux = serializer.data
                    data_aux["category"] = audio.category.name
                    return JSONResponse(data_aux, status=201)
                remove_record(data['path'])
                response_data_save["details"] = serializer.errors
                return JSONResponse(response_data_save, status=400)

        except Exception or KeyError or ValueError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


# Método para obtener listado de audios de un sitio que pertenece a una categoría concreta
@csrf_exempt
def audio_site_category_get(request, site_id):
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}
    response_category_not_found = {"error": "CATEGORY_NOT_FOUND", "details": "The category does not exist"}
    response_audio_get = {"error": "GET_AUDIO", "details": "THe was an error to get the audios"}

    try:
        site_found = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'GET':

        try:

            category_names = request.GET.get('categories')

            audios_list = []
            categories_list = []
            for category_name in category_names.split(","):
                try:

                    category_found = Category.objects.get(name=category_name)
                    categories_list.append(category_found)
                except Category.DoesNotExist:
                    return JSONResponse(response_category_not_found, status=404)

            audios = Audio.objects.all().filter(category__in=categories_list, site=site_found)
            audios_list.extend(audios)

            serializer = AudioSerializer(audios_list, many=True)

        except Exception or KeyError or ValueError as e:
            response_audio_get["details"] = str(e)
            return JSONResponse(response_audio_get, status= 400)

        return JSONResponse(serializer.data, status=200)

    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
@transaction.atomic
def audio_listen(request, audio_id):

    response_audio_not_found = {"error": "AUDIO_NOT_FOUND", "details": "The audio does not exit"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_data_save = {"error": "LISTEN_AUDIO", "details": "There was an error to listen audio"}

    if request.method == 'PUT':

        try:
            audio = Audio.objects.get(pk=audio_id)
        except Audio.DoesNotExist:
            return JSONResponse(response_audio_not_found, status=404)

        try:
            with transaction.atomic():

                audio.numberReproductions = audio.numberReproductions + 1

                # Save the audio
                audio.save()

                # Update in Firebase
                update_audio(audio)

                return HttpResponse(status=204)

        except Exception or KeyError or ValueError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method,
                            status=400)


@csrf_exempt
@transaction.atomic
def advertisement_listen(request, advertisement_id):

    response_advertisement_not_found = {"error": "ADVERTISEMENT_NOT_FOUND", "details": "The advertisement does not exit"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_data_save = {"error": "LISTEN_ADVERTISEMENT", "details": "There was an error to listen advertisement"}

    if request.method == "PUT":

        try:
            ad = Advertisement.objects.get(pk=advertisement_id)
        except Advertisement.DoesNotExist:
            return JSONResponse(response_advertisement_not_found, status=404)

        try:

            # logged actor
            with transaction.atomic():

                ad.numberReproductions = ad.numberReproductions + 1

                duration = get_record_duration(ad.path)

                configuration = Configuration.objects.all()[0]

                # comprobar que se le suma solo a un usuario logueado o a un anunciante que no escucha su propio audio
                login_result = login(request, 'user')
                login_result2 = login(request, 'advertiser')

                if login_result is True or login_result2 is True:
                    actor = Actor.objects.get(user_account=request.user.id)
                    if (login_result is True) or (login_result2 is True and ad.actor.id != actor.id):
                        today = date.today()
                        reproduction = Reproduction.objects.filter(actor__user_account=request.user.id).filter(advertisement=ad.id).filter(date__month=today.month, date__year=today.year, date__day=today.day)
                        if len(reproduction) == 0:
                            data_reproduction = {}
                            data_reproduction['actor'] = actor.id
                            data_reproduction['advertisement'] = ad.id
                            data_reproduction['date'] = datetime.now()
                            serializer = ReproductionSerializer(data=data_reproduction)
                            if serializer.is_valid():
                                serializer.save()
                                actor.minutes = actor.minutes + int(configuration.time_listen_advertisement * duration)
                                actor.save()
                                reproductions = Reproduction.objects.filter(advertisement=ad.id).filter(date__month=today.month, date__year=today.year)
                                if len(reproductions) >= round((ad.maxPriceToPay*10000)/(int(duration)*ad.radius)):
                                    ad.isActive = False
                            else:
                                response_data_save["details"] = serializer.errors
                                return JSONResponse(response_data_save, status=400)

                # Save the audio
                ad.save()

                # Update in Firebase
                update_advertisement(ad)

                return HttpResponse(status=204)

        except Exception or ValueError or KeyError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


# Metodos auxiliares
def pruned_serializer_advertisement_update(advertisement, data):
    data["latitude"] = advertisement.latitude
    data["longitude"] = advertisement.longitude
    data["numberReproductions"] = advertisement.numberReproductions
    data["path"] = advertisement.path
    data["duration"] = advertisement.duration
    data["radius"] = advertisement.radius
    data["isActive"] = advertisement.isActive
    data["actor"] = advertisement.actor.id
    return data


def pruned_serializer_advertisement_create(data):
    data["numberReproductions"] = 0
    data["isActive"] = True
    data["isDelete"] = False
    data["duration"] = get_record_duration(data["path"])
    return data


def pruned_serializer_audio_create(data):
    time_now = datetime.now()
    time = time_now + timedelta(seconds=get_object_or_404(Category, name=data['category']).minDurationMap)
    data['timestampFinish'] = time
    data['timestampCreation'] = time_now
    data['isInappropriate'] = False
    data["numberReproductions"] = 0
    data['category'] = get_object_or_404(Category, name=data['category']).pk
    data["duration"] = get_record_duration(data["path"])
    return data


def pruned_serializer_audio_create_site(data, site_id):
    site = Site.objects.get(pk=site_id)
    time_now = datetime.now()
    time = time_now + timedelta(seconds=get_object_or_404(Category, name=data['category']).minDurationMap)
    data['latitude'] = site.latitude
    data['longitude'] = site.longitude
    data['timestampFinish'] = time
    data['timestampCreation'] = time_now
    data['isInappropriate'] = False
    data["numberReproductions"] = 0
    data["duration"] = get_record_duration(data["path"])
    data['category'] = get_object_or_404(Category, name=data['category']).pk
    return data


@csrf_exempt
@transaction.atomic
def like_create(request, audio_id):

    response_data_save = {"error": "SAVE_LIKE", "details": "There was an error to save the like"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_liked = {"error": "ALREADY_LIKED", "details": "This user has already liked the audio"}

    if request.method == 'POST':

        login_result = login(request, 'advertiserUser')
        if login_result is not True:
            return login_result

        try:
            with transaction.atomic():

                data = {}
                actor = Actor.objects.get(user_account=request.user.id)
                data['actor'] = actor.id
                data['audio'] = audio_id

                serializer = LikeSerializer(data=data)

                audio = Audio.objects.get(id=audio_id)
                audio.timestampFinish = audio.timestampFinish + timedelta(
                    seconds=Configuration.objects.all()[0].time_extend_audio)

                if len(Like.objects.filter(audio=audio_id).filter(actor__user_account=request.user.id)) != 0:
                    return JSONResponse(response_liked, status=400)

                if serializer.is_valid():
                    # Save in db
                    serializer.save()
                    audio.save()
                    # Update in Firebase
                    update_audio(audio)

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
def report_create(request, audio_id):

    response_data_save = {"error": "SAVE_REPORT", "details": "There was an error to save the report"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_reported = {"error": "ALREADY_REPORTED", "details": "This user has already reported the audio"}

    if request.method == 'POST':

        login_result = login(request, 'advertiserUser')
        if login_result is not True:
            return login_result

        try:
            with transaction.atomic():
                configuration = Configuration.objects.all()[0]
                data = {}
                actor = Actor.objects.get(user_account=request.user.id)
                data['actor'] = actor.id
                # Fin user de prueba
                data['audio'] = audio_id
                serializer = ReportSerializer(data=data)

                if len(Report.objects.filter(audio=audio_id).filter(actor__user_account=request.user.id)) != 0:
                    return JSONResponse(response_reported, status=400)

                if serializer.is_valid():
                    # Save in db
                    report = serializer.save()
                    reports = Report.objects.filter(audio=audio_id)
                    if len(reports) >= configuration.minimum_reports_ban and report.audio.isInappropriate is False:
                        audio = report.audio
                        audio.isInappropriate = True
                        audio.save()
                        # Update in Firebase
                        update_audio(audio)
                    return JSONResponse(serializer.data, status=201)
                response_data_save["details"] = serializer.errors
                return JSONResponse(response_data_save, status=400)

        except Exception or ValueError or KeyError as e:
            response_data_save["details"] = str(e)
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


