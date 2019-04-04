from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from .models import Tag
from .serializers import TagSerializer
from rest_framework.renderers import JSONRenderer
from django.db import transaction
from django.http import HttpResponse


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
def get_all_tags(request):

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_tags_get = {"error": "GET_TAGS", "details": "There was an error to get all tags"}

    if request.method == 'GET':

        try:

            tags = Tag.objects.all()
            serializer = TagSerializer(tags, many=True)
            data_aux = serializer.data

        except Exception or ValueError or KeyError:
            return JSONResponse(response_tags_get, status=400)

        return JSONResponse(data_aux)

    else:
        return JSONResponse(response_data_not_method,
                            status=400)
