from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Advertisement
from .serializers import AdvertisementSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def advertisement_create(request):
    response_data_save = {"error": "Error to save the advertisement", "details": "There was an error to save the "
                                                                                 "advertisement"}
    response_data_not_method = {"error": "Incorrect method", "details": "The method is incorrect"}

    if request.method == 'POST':
        data = JSONParser().parse(request)
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
def advertisement_update_get(request, advertisement_id):
    """
    Retrieve, get,update advertisement.
    """
    response_data_put = {"error": "Error to update the advertisement", "details": "There was an error to "                                                                    
                                                                                  "update the advertisement"}
    response_data_not_method = {"error": "Incorrect method", "details": "The method is incorrect"}
    response_advertisement_not_found = {"error": "Advertisement not found", "details": "The advertisement doesn't exit"}
    try:
        advertisement = Advertisement.objects.get(pk=advertisement_id)
    except Advertisement.DoesNotExist:
        return JSONResponse(response_advertisement_not_found, status=400)

    if request.method == 'GET':
        serializer = AdvertisementSerializer(advertisement)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        data = pruned_serializer_advertisement_update(advertisement, data)
        serializer = AdvertisementSerializer(advertisement, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(response_data_put, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)


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
