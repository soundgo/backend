from django.shortcuts import render

from .models import Configuration
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .serializers import ConfigurationSerializer
# Create your views here.

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def configuration_get(request):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_configuration_not_found = {"error": "CONFIGURATION_NOT_FOUND", "details": "The configuration does not exit"}

    response_configuration_get = {"error": "GET_CONFIGURATION", "details": "There was an error to get the configuration"}


    try:
        configuration = Configuration.objects.all()[0]
    except Configuration.DoesNotExist:
        return JSONResponse(response_configuration_not_found, status=404)

    if request.method == 'GET':

        try:

            serializer = ConfigurationSerializer(configuration)

        except Exception or ValueError or KeyError as e:
            return JSONResponse(str(e), status=400)

        return JSONResponse(serializer.data)


    else:
        return JSONResponse(response_data_not_method,
                            status=400)
