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

from requests import post, put, delete
from requests.exceptions import RequestException
import schedule
import time


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

        # TODO coger el base 64 y guardar , meter en data['path'] la url que retorne
        # TODO guardar en mapbox el advertisement

        data = pruned_serializer_advertisement_create(data)
        serializer = AdvertisementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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

        #Si lo quiere borrar se va a marcar como borrado y se borra de mapbox y del servidor
        if data['isDelete']:
            pass
            # TODO Borrar audio de mapbox
            # TODO Borrar audio de servidor

        data = pruned_serializer_advertisement_update(advertisement, data)
        serializer = AdvertisementSerializer(advertisement, data=data)
        if serializer.is_valid():
            serializer.save()
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

        #TODO coger el base 64 y guardar , meter en data['path'] la url que retorne


        data = pruned_serializer_audio_create(data)
        serializer = AudioSerializer(data=data)

        if serializer.is_valid():
            audio= serializer.save()
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

    try:
        audio = Audio.objects.get(pk=audio_id)
    except Audio.DoesNotExist:
        return JSONResponse(response_audio_not_found, status=404)


    if request.method == 'GET':
        serializer = AudioSerializer(audio)
        return JSONResponse(serializer.data)

    elif request.method == 'DELETE':
        delete_mapbox(audio.category.name, audio.id)
        #TODO Borrar audio de servidor

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

        # TODO coger el base 64 y guardar , meter en data['path'] la url que retorne
        # TODO guardar en mapbox el audio

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


def create_mapbox(category, latitude, longitude, idRecord):
    # Mapbox configuration
    datasetMap = {"site": "cjtke1edi02q02wn5kjd9en24", "leisure": "cjtkadw8e03jy4fnycl0ue5cn",
                  "experience": "cjtkae6lv0phe2xtg8u2jiny9", "tourism": "cjtkaesz804254bodwfnw63r6",
                  "advertisement": "cjtkacy841h2g2wllukp7sfij"}
    token = "sk.eyJ1Ijoic291bmRnbyIsImEiOiJjanRrYzl0a3YwZ3ljM3lxamVqYmhidjJmIn0.zwUJZmYb3qrhsLoPN-Xqrw"
    idDataset = datasetMap[category.lower()]

    url= "https://api.mapbox.com/datasets/v1/soundgo/"+idDataset+"/features/"+str(idRecord)+"?access_token="+token
    params= {
        "id": str(idRecord),
        "geometry": {
            "coordinates": [
              float(latitude),
              float(longitude)
            ],
            "type": "Point"
        },
        "type": "Feature",
        "properties": {

        }
    }

    try:
        request= put(url, json= params)
        response = request.text
    except RequestException:
        response = "Error saving record in mapbox"


    return response

def delete_mapbox(category, idRecord):
    # Mapbox configuration
    datasetMap = {"site": "cjtke1edi02q02wn5kjd9en24", "leisure": "cjtkadw8e03jy4fnycl0ue5cn",
                  "experience": "cjtkae6lv0phe2xtg8u2jiny9", "tourism": "cjtkaesz804254bodwfnw63r6",
                  "advertisement": "cjtkacy841h2g2wllukp7sfij"}
    token = "sk.eyJ1Ijoic291bmRnbyIsImEiOiJjanRrYzl0a3YwZ3ljM3lxamVqYmhidjJmIn0.zwUJZmYb3qrhsLoPN-Xqrw"
    idDataset = datasetMap[category.lower()]

    url = "https://api.mapbox.com/datasets/v1/soundgo/" + idDataset + "/features/" + str(idRecord) + "?access_token=" + token


    try:
        request = delete(url)
        response = request.text
    except RequestException:
        response = "Error deleting record in mapbox"


    return response




def update_mapbox():

    # Mapbox configuration
    datasetMap = {"site": "cjtke1edi02q02wn5kjd9en24", "leisure": "cjtkadw8e03jy4fnycl0ue5cn",
                  "experience": "cjtkae6lv0phe2xtg8u2jiny9", "tourism": "cjtkaesz804254bodwfnw63r6",
                  "advertisement": "cjtkacy841h2g2wllukp7sfij"}
    tilesetMap = {"site": "soundgo.sites", "leisure": "soundgo.leisure", "experience": "soundgo.experience",
                  "tourism": "soundgo.tourism", "advertisement": "soundgo.ads"}
    token = "sk.eyJ1Ijoic291bmRnbyIsImEiOiJjanRrYzl0a3YwZ3ljM3lxamVqYmhidjJmIn0.zwUJZmYb3qrhsLoPN-Xqrw"

    for key, value in datasetMap.items():
        idDataset = datasetMap[key]
        idTileset = tilesetMap[key]

        url = "https://api.mapbox.com/uploads/v1/soundgo?access_token="+token
        params = {
            "tileset": idTileset,
            "url": "mapbox://datasets/soundgo/"+idDataset,
            "name": idTileset.split(".")[1]
        }


        try:
            request = post(url, json=params)
            response = request.text
        except RequestException:
            response = "Error saving record in mapbox"



    return response




def mapbox_update():
    schedule.every().minute.do(update_mapbox)

    while True:
        schedule.run_pending()
        time.sleep(1)

