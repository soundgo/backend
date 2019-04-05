from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Site
from accounts.models import Actor
from .serializers import SiteSerializer
from django.db import transaction
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

        try:

            data = JSONParser().parse(request)

            # TODO user de prueba, para que se cree tiene que ser un usuario con tarjeta o ser administrador
            actor = Actor.objects.all()[0]
            data['actor'] = actor.id
            # Fin user de prueba

            serializer = SiteSerializer(data=data)
            if serializer.is_valid():
                # Save in db
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(response_data_save, status=400)

        except Exception or ValueError or KeyError as e:
            return JSONResponse(str(e), status=400)

    else:
        return JSONResponse(response_data_not_method, status=400)


@csrf_exempt
@transaction.atomic
def site_update_delete_get(request, site_id):
    """
    Retrieve, get,update,delete a site.
    """
    response_data_put = {"error": "UPDATE_SITE", "details": "There was an error to update the site"}

    response_data_get = {"error": "GET_SITE", "details": "There was an error to get the site"}

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}

    response_data_delete = {"error": "DELETE_SITE", "details": "There was an error to delete the site"}

    try:
        site = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'GET':

        try:

            serializer = SiteSerializer(site)

        except Exception or ValueError or KeyError as e:
            return JSONResponse(str(e), status=400)

        data_aux = serializer.data
        data_aux.pop("actor")
        data_aux["name_actor"] = site.actor.user_account.nickname
        data_aux["photo"] = site.actor.photo
        return JSONResponse(data_aux, status=200)

    # Todo solo lo puede actualizar y borrar el advertiser del anuncio y el administrador

    elif request.method == 'PUT':

        try:

            data = JSONParser().parse(request)
            data = pruned_serializer_site_update(site, data)
            serializer = SiteSerializer(site, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)

        except Exception or ValueError or KeyError as e:
            return JSONResponse(str(e), status=400)

        return JSONResponse(response_data_put, status=400)

    elif request.method == 'DELETE':

        try:

            # Remove site from db
            site.delete()

        except Exception or KeyError or ValueError as e:
            return JSONResponse(str(e), status=400)

        return HttpResponse(status=204)

    else:
        return JSONResponse(response_data_not_method, status=400)


def pruned_serializer_site_update(site, data):
    data["latitude"] = site.latitude
    data["longitude"] = site.longitude
    data["actor"] = site.actor.id

    return data
