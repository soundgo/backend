from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Advertisement, Audio, Category
from accounts.models import Language
from sites.models import Site
from .serializers import AdvertisementSerializer, AudioSerializer
from datetime import timedelta
from datetime import datetime
from django.db import transaction
from .mapbox_manager import create_mapbox, delete_mapbox
from .cloudinary_records_manager import upload_record, remove_record



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
    response_data_save = {"error": "SAVE_ADVERTISEMENT", "details": "There was an error to save the "
                                                                                 "advertisement"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    if request.method == 'POST':
        data = JSONParser().parse(request)

        #coger el base 64 y guardar , meter en data['path'] la url que retorne
        data['path']= upload_record(data['base64'])

        data = pruned_serializer_advertisement_create(data)
        serializer = AdvertisementSerializer(data=data)
        if serializer.is_valid():
            advertisement= serializer.save()

            #Guardar en mapbox
            create_mapbox("advertisement", advertisement.latitude, advertisement.longitude, advertisement.id)
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method,
                            status=400)


@csrf_exempt
@transaction.atomic
def advertisement_update_get(request, advertisement_id):

    response_data_put = {"error": "UPDATE_ADVERTISEMENT", "details": "There was an error to "                                                                                                                                                 
                                                                     "update the advertisement"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_advertisement_not_found = {"error": "ADVERTISEMENT_NOT_FOUND", "details": "The advertisement does not exit"}

    try:
        advertisement = Advertisement.objects.get(pk=advertisement_id)
    except Advertisement.DoesNotExist:
        return JSONResponse(response_advertisement_not_found, status=404)

    if request.method == 'GET':
        serializer = AdvertisementSerializer(advertisement)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)

        data = pruned_serializer_advertisement_update(advertisement, data)
        serializer = AdvertisementSerializer(advertisement, data=data)
        if serializer.is_valid():
            serializer.save()

            # Si lo quiere borrar se va a marcar como borrado y se borra de mapbox y del servidor
            if data['isDelete']:
                # Borrar audio de servidor
                result = remove_record(advertisement.path)
                if not result:
                    raise Exception(response_data_put)

                # Borrar audio de mapbox
                delete_mapbox(advertisement.category.name, advertisement.id)

            return JSONResponse(serializer.data)
        return JSONResponse(response_data_put, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)


#Metodos audios
@csrf_exempt
@transaction.atomic
def audio_create(request):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_data_save = {"error": "SAVE_AUDIO", "details": "There was an error to save the audio"}

    if request.method == 'POST':

        data = JSONParser().parse(request)

        #Coger el base 64 y guardar , meter en data['path'] la url que retorne
        data['path'] = upload_record(data['base64'])


        data = pruned_serializer_audio_create(data)
        serializer = AudioSerializer(data=data)

        if serializer.is_valid():
            audio= serializer.save()

            #Guardar en mapbox
            create_mapbox(audio.category.name, audio.latitude, audio.longitude, audio.id)
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method,
                            status=400)

@csrf_exempt
@transaction.atomic
def audio_delete_get(request, audio_id):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_audio_not_found = {"error": "AUDIO_NOT_FOUND", "details": "The audio does not exit"}
    response_audio_not_delete = {"error": "AUDIO_NOT_DELETE", "details": "The audio can not delete"}

    try:
        audio = Audio.objects.get(pk=audio_id)
    except Audio.DoesNotExist:
        return JSONResponse(response_audio_not_found, status=404)


    if request.method == 'GET':
        serializer = AudioSerializer(audio)
        return JSONResponse(serializer.data)

    elif request.method == 'DELETE':

        #Borramos de mapbox
        delete_mapbox(audio.category.name, audio.id)

        #Borramos del servidor
        result = remove_record(audio.path)
        if not result:
            raise Exception(response_audio_not_delete)

        audio.delete()
        return HttpResponse(status=204)
    else:
        return JSONResponse(response_data_not_method,
                            status=400)


#Metodo site
@csrf_exempt
@transaction.atomic
def audio_site_create_get(request, site_id):
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}
    response_data_save = {"error": "SAVE_AUDIO", "details": "There was an error to save the audio"}

    try:
        site= Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data = pruned_serializer_audio_create(data)
        # Metemos en el audio el site
        data['site'] = site_id
        serializer = AudioSerializer(data=data)


        # Coger el base 64 y guardar , meter en data['path'] la url que retorne
        data['path'] = upload_record(data['base64'])
        # Este audio no se guarda en mapbox, en mapbox estará el sitio


        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(response_data_save, status=400)

    elif request.method == 'GET':

        audios= site.records
        serializer = AudioSerializer(audios, many=True)

        return JSONResponse(serializer.data)

    else:
        return JSONResponse(response_data_not_method,
                            status=400)


#Metodos auxiliares
def pruned_serializer_advertisement_update(advertisement, data):
    data["latitude"] = advertisement.latitude
    data["longitude"] = advertisement.longitude
    data["numberReproductions"] = advertisement.numberReproductions
    data["path"] = advertisement.path
    data["radius"] = advertisement.radius
    data["isActive"] = advertisement.isActive
    return data


def pruned_serializer_advertisement_create(data):
    data["numberReproductions"] = 0
    data["isActive"] = True
    data["isDelete"] = False
    return data


def pruned_serializer_audio_create(data):
    timeNow= datetime.now()
    time = timeNow + timedelta(seconds=get_object_or_404(Category, name=data['category']).minDurationMap)
    data['timestampFinish'] = time
    data['timestampCreation'] = timeNow
    data['isInappropriate'] = False
    data["numberReproductions"] = 0
    data['category']= get_object_or_404(Category, name=data['category']).pk
    data['language'] = get_object_or_404(Language, name=data['language']).pk
    return data




