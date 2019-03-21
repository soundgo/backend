from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Site
from .serializers import SiteSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def site_create(request):
    response_data_save = {"error": "Error to save the site", "details": "There was an error to save the "
                                                                        "site"}
    response_data_not_method = {"error": "Incorrect method", "details": "The method is incorrect"}

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SiteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
def site_update_delete_get(request, site_id):
    """
    Retrieve, get,update,delete a site.
    """
    response_data_put = {"error": "Error to update the site", "details": "There was an error to update the site"}

    response_data_not_method = {"error": "Incorrect method", "details": "The method is incorrect"}

    response_site_not_found = {"error": "Site not found", "details": "The site doesn't exit"}

    try:
        site = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=400)

    if request.method == 'GET':
        serializer = SiteSerializer(site)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SiteSerializer(site, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(response_data_put, status=400)

    elif request.method == 'DELETE':
        site.delete()
        return HttpResponse(status=204)

    else:
        return JSONResponse(response_data_not_method, status=400)
