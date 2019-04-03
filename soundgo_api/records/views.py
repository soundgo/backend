from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Advertisement, Audio, Category, Like
from sites.models import Site
from .serializers import AdvertisementSerializer, AudioSerializer, LikeSerializer
from datetime import timedelta
from datetime import datetime
from django.db import transaction
from managers.cloudinary_manager import upload_record, remove_record, get_record_duration
from accounts.models import Actor
from accounts.views import login
from managers.firebase_manager import add_audio, add_advertisement, remove_audio, remove_advertisement
from copy import deepcopy
from configuration.models import Configuration
from datetime import timedelta

# TODO comprobar que el usuario puede actualizar, borrar y crear cada objeto


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

    if request.method == 'POST':

        try:

            data = JSONParser().parse(request)

            # TODO user de prueba. Comprobar que tenga tarjeta de credito, lo crea el usuario autenticado si es anunciante
            actor = Actor.objects.all()[0]
            data['actor'] = actor.id
            # Fin user de prueba

            # coger el base 64 y guardar , meter en data['path'] la url que retorne
            try:
                data['path'] = upload_record(data['base64'])
                data = pruned_serializer_advertisement_create(data)
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
            return JSONResponse(response_data_save, status=400)

        except Exception or KeyError or ValueError as e:
            return JSONResponse(response_data_save, status=400)

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

    try:
        advertisement = Advertisement.objects.get(pk=advertisement_id)
    except Advertisement.DoesNotExist:
        return JSONResponse(response_advertisement_not_found, status=404)

    if request.method == 'GET':

        try:

            serializer = AdvertisementSerializer(advertisement)

        except Exception or ValueError or KeyError:
            return JSONResponse(response_data_get, status= 400)

        data_aux = serializer.data
        data_aux.pop('actor')
        data_aux["name"] = advertisement.actor.user_account.nickname
        data_aux["photo"] = advertisement.actor.photo
        return JSONResponse(data_aux)

    elif request.method == 'PUT':

        try:

            # Todo poner que el que lo modifica es el mismo que lo crea
            if advertisement.isDelete is True:
                return JSONResponse(response_data_deleted, status=400)

            data = JSONParser().parse(request)

            data = pruned_serializer_advertisement_update(advertisement, data)
            serializer = AdvertisementSerializer(advertisement, data=data)
            if serializer.is_valid():
                serializer.save()

                # Si lo quiere borrar se va a marcar como borrado y se borra de mapbox y del servidor
                if data['isDelete']:
                    # Borrar grabacion de servidor
                    result = remove_record(advertisement.path)
                    if not result:
                        return JSONResponse(response_data_put, status=400)
                    # Remove advertisement from Firebase Cloud Firestore
                    remove_advertisement(advertisement)

                return JSONResponse(serializer.data)
            return JSONResponse(response_data_put, status=400)

        except Exception or ValueError or KeyError as e:
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

    if request.method == 'POST':

        try:

            print(request)
            data = JSONParser().parse(request)

            # TODO user de prueba, poner que el que lo crea es el usuario autenticado
            actor = Actor.objects.all()[0]
            data['actor'] = actor.id
            # Fin user de prueba

            # Coger el base 64 y guardar , meter en data['path'] la url que retorne
            try:
                data['path'] = upload_record(data['base64'])

                data = pruned_serializer_audio_create(data)
                serializer = AudioSerializer(data=data)
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
                # Save in db
                audio = serializer.save()
                # Save in Firebase Cloud Firestore
                add_audio(audio)
                #Save actor with new minutes
                actor.save()
                data_aux = serializer.data
                data_aux["category"] = audio.category.name
                return JSONResponse(data_aux, status=201)
            remove_record(data['path'])
            return JSONResponse(response_data_save, status=400)

        except Exception or KeyError or ValueError as e:
            return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method,
                            status=400)


@csrf_exempt
@transaction.atomic
def audio_delete_get(request, audio_id):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_audio_not_found = {"error": "AUDIO_NOT_FOUND", "details": "The audio does not exit"}
    response_audio_not_delete = {"error": "AUDIO_NOT_DELETE", "details": "The audio cannot be deleted"}
    response_audio_get = {"error": "GET_AUDIO", "details": "There was an error to get the audio"}
    response_audio_delete = {"error": "DELETE_AUDIO", "details": "There was an error to delete the audio"}

    try:
        audio = Audio.objects.get(pk=audio_id)
    except Audio.DoesNotExist:
        return JSONResponse(response_audio_not_found, status=404)

    if request.method == 'GET':

        try:

            login(request, 'all')
            serializer = AudioSerializer(audio)
            data_aux = serializer.data
            data_aux["category"] = audio.category.name
            data_aux.pop("actor")
            data_aux["name"] = audio.actor.user_account.nickname
            data_aux["photo"] = audio.actor.photo
            data_aux["numberLikes"] = len(Like.objects.filter(audio=audio_id))
            if len(Like.objects.filter(audio=audio_id).filter(actor=request.user.id)) == 0:
                data_aux["liked"] = False
            else:
                data_aux["liked"] = True

        except Exception or ValueError or KeyError:
            return JSONResponse(response_audio_get, status=400)

        return JSONResponse(data_aux)

    elif request.method == 'DELETE':

        try:

            # Todo Solo lo puede borrar el creador del audio o un administrador
            audio_copy = deepcopy(audio)
            audio.delete()
            # Remove audio from Firebase Cloud Firestore
            try:
                remove_audio(audio_copy)
            except Exception:
                pass
            finally:
                # Borramos del servidor
                result = remove_record(audio_copy.path)
                if not result:
                    return JSONResponse(response_audio_not_delete, status=400)

        except Exception or KeyError or ValueError:
            return JSONResponse(response_audio_delete, status = 400)

        return HttpResponse(status=204)

    else:
        return JSONResponse(response_data_not_method,
                            status=400)


# Metodo site
@csrf_exempt
@transaction.atomic
def audio_site_create(request, site_id):
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}
    response_data_save = {"error": "SAVE_AUDIO", "details": "There was an error to save the audio"}
    response_data_not_minutes = {"error": "NOT_MINUTES", "details": "You do not have enough time to record this audio"}

    try:
        Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'POST':

        try:

            data = JSONParser().parse(request)

            # TODO user de prueba, el creador del audio es el usuario autenticado
            actor = Actor.objects.all()[0]
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


            # Este audio no se guarda en mapbox, en mapbox estará el sitio

            if serializer.is_valid():
                audio = serializer.save()
                actor.save()
                data_aux = serializer.data
                data_aux["category"] = audio.category.name
                return JSONResponse(data_aux, status=201)
            remove_record(data['path'])
            return JSONResponse(response_data_save, status=400)

        except Exception  or KeyError or ValueError as e:
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

        except Exception or KeyError or ValueError:
            return JSONResponse(response_audio_get, status= 400)

        return JSONResponse(serializer.data)

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

            audio.numberReproductions = audio.numberReproductions + 1

            # Save the audio
            audio.save()

            return HttpResponse(status=204)

        except Exception or KeyError or ValueError:
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
                # TODO user de prueba, hay que coger el user logueado y en el futuro comprobar si no lo ha escuchado ya ese día el anuncio
                # TODO si estas logueado solo puedes escuchar el anuncio una vez al día (esto cómo se controla, me manda primero una petición al get y devuelvo si el autenticado lo puede escuchar?),
                #  y si es la primera vez que lo escuchas se crea un reproduction
                # TODO  (PROPUESTA) si el usuario es un administrador o es el mismo creador del audio debe poder escucharlo siempre y no se suma ni reproducciones ni minutos.

            actor = Actor.objects.all()[0]

            ad.numberReproductions = ad.numberReproductions + 1

            duration = get_record_duration(ad.path)

            configuration = Configuration.objects.all()[0]

            actor.minutes = actor.minutes + int(configuration.time_listen_advertisement * duration)

            # Save the audio
            ad.save()
            actor.save()

            return HttpResponse(status=204)

        except Exception or ValueError or KeyError:
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


# Metodos auxiliares
def pruned_serializer_advertisement_update(advertisement, data):
    data["latitude"] = advertisement.latitude
    data["longitude"] = advertisement.longitude
    data["numberReproductions"] = advertisement.numberReproductions
    data["path"] = advertisement.path
    data["radius"] = advertisement.radius
    data["isActive"] = advertisement.isActive
    data["actor"] = advertisement.actor.id
    return data


def pruned_serializer_advertisement_create(data):
    data["numberReproductions"] = 0
    data["isActive"] = True
    data["isDelete"] = False
    return data


def pruned_serializer_audio_create(data):
    time_now = datetime.now()
    time = time_now + timedelta(seconds=get_object_or_404(Category, name=data['category']).minDurationMap)
    data['timestampFinish'] = time
    data['timestampCreation'] = time_now
    data['isInappropriate'] = False
    data["numberReproductions"] = 0
    data['category'] = get_object_or_404(Category, name=data['category']).pk
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
    data['category'] = get_object_or_404(Category, name=data['category']).pk
    return data


@csrf_exempt
@transaction.atomic
def like_create(request, audio_id):

    response_data_save = {"error": "SAVE_LIKE", "details": "There was an error to save the like"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    if request.method == 'POST':

        loginResult = login(request, 'advertiserUser')
        if loginResult != True:
            return loginResult

        try:

            data = {}

            data['actor'] = request.user.id
            data['audio'] = audio_id

            serializer = LikeSerializer(data=data)

            audio = Audio.objects.get(id=audio_id)
            audio.timestampFinish = audio.timestampFinish + timedelta(
                seconds=Configuration.objects.all()[0].time_extend_audio)
            if serializer.is_valid():
                # Save in db
                serializer.save()
                audio.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(response_data_save, status=400)

        except Exception or ValueError or KeyError:
            return JSONResponse(response_data_save, status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)
