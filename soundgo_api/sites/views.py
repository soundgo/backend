from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Site
from accounts.models import Actor
from .serializers import SiteSerializer
from django.db import transaction
from managers.firebase_manager import add_site, remove_site
from copy import deepcopy


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
def site_create(request):

    response_data_save = {"error": "SAVE_SITE", "details": "There was an error to save the site"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    if request.method == 'POST':
        data = JSONParser().parse(request)

        # TODO user de prueba, para que se cree tiene que ser un usuario con tarjeta o ser administrador
        actor = Actor.objects.all()[0]
        data['actor'] = actor.id
        # Fin user de prueba

        serializer = SiteSerializer(data=data)
        if serializer.is_valid():
            # Save in db
            site = serializer.save()
            # Save in Firebase Cloud Firestore
            add_site(site)
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(response_data_save, status=400)
    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
@transaction.atomic
def site_update_delete_get(request, site_id):
    """
    Retrieve, get,update,delete a site.
    """
    response_data_put = {"error": "UPDATE_SITE", "details": "There was an error to update the site"}

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}

    try:
        site = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'GET':
        serializer = SiteSerializer(site)
        return JSONResponse(serializer.data)

    # Todo solo lo puede actualizar y borrar el advertiser del anuncio y el administrador

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        data = pruned_serializer_site_update(site, data)
        serializer = SiteSerializer(site, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(response_data_put, status=400)

    elif request.method == 'DELETE':
        # Remove site from Firebase Cloud Firestore
        site_copy = deepcopy(site)
        # Remove site from db
        site.delete()
        remove_site(site_copy)
        return HttpResponse(status=204)

    else:
        return JSONResponse(response_data_not_method, status=400)


def pruned_serializer_site_update(site, data):
    data["latitude"] = site.latitude
    data["longitude"] = site.longitude
    data["actor"] = site.actor.id

    return data
