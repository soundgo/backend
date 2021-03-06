from accounts.models import Actor
from accounts.views import login
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

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
@transaction.atomic
def get_all_sites(request):
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_sites_get = {"error": "GET_SITES", "details": "There was an error to get all sites"}

    if request.method == 'GET':

        try:

            sites = Site.objects.all()
            data_auxs = []

            for site in sites:
                serializer = SiteSerializer(site)
                data_aux = serializer.data
                data_aux.pop("actor")
                data_aux["name_actor"] = site.actor.user_account.nickname
                data_aux["photo"] = site.actor.photo
                data_auxs.append(data_aux)

        except Exception or ValueError or KeyError as e:
            response_sites_get["details"] = str(e)
            return JSONResponse(response_sites_get, status=400)

        return JSONResponse(data_auxs)

    else:
        return JSONResponse(response_data_not_method,
                            status=400)


@csrf_exempt
@transaction.atomic
def site_create(request):
    response_data_save = {"error": "SAVE_SITE", "details": "There was an error to save the site"}
    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}
    response_actor_not_credit_card = {"error": "ACTOR_NOT_CREDIT_CARD",
                                      "details": "Logged user does not have a credit card"}

    if request.method == 'POST':

        try:
            with transaction.atomic():

                data = JSONParser().parse(request)

                # comprobar que tiene que ser un anunciante con tarjeta o ser administrador

                login_result = login(request, 'advertiser')
                login_result2 = login(request, 'admin')

                if login_result is not True and login_result2 is not True:
                    return login_result

                if login_result is True:
                    actor_aux = Actor.objects.get(user_account=request.user.id)
                    if actor_aux.credit_card is None:
                        return JSONResponse(response_actor_not_credit_card, status=400)

                actor = Actor.objects.get(user_account=request.user.id)
                data['actor'] = actor.id
                # Fin user de prueba

                serializer = SiteSerializer(data=data)
                if serializer.is_valid():
                    # Save in db
                    serializer.save()
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
def site_update_delete_get(request, site_id):
    """
    Retrieve, get,update,delete a site.
    """
    response_data_put = {"error": "UPDATE_SITE", "details": "There was an error to update the site"}

    response_data_get = {"error": "GET_SITE", "details": "There was an error to get the site"}

    response_data_not_method = {"error": "INCORRECT_METHOD", "details": "The method is incorrect"}

    response_site_not_found = {"error": "SITE_NOT_FOUND", "details": "The site does not exit"}

    response_data_delete = {"error": "DELETE_SITE", "details": "There was an error to delete the site"}

    response_site_not_belong = {"error": "SITE_NOT_BELONG", "details": "The site does not belong to the logged user"}

    try:
        site = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JSONResponse(response_site_not_found, status=404)

    if request.method == 'GET':

        try:

            serializer = SiteSerializer(site)

        except Exception or ValueError or KeyError as e:
            response_data_get["details"] = str(e)
            return JSONResponse(response_data_get, status=400)

        data_aux = serializer.data
        data_aux.pop("actor")
        data_aux["name_actor"] = site.actor.user_account.nickname
        data_aux["photo"] = site.actor.photo
        return JSONResponse(data_aux, status=200)

    # Comprobar que solo lo puede actualizar y borrar el advertiser del anuncio y el administrador

    elif request.method == 'PUT':

        login_result = login(request, 'advertiser')
        login_result2 = login(request, 'admin')

        if login_result is not True and login_result2 is not True:
            return login_result

        if login_result is True:
            actor_aux = Actor.objects.get(user_account=request.user.id)
            if site.actor.id != actor_aux.id:
                return JSONResponse(response_site_not_belong, status=400)

        try:
            with transaction.atomic():
                data = JSONParser().parse(request)
                data = pruned_serializer_site_update(site, data)
                serializer = SiteSerializer(site, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data)
                response_data_put["details"] = serializer.errors
                return JSONResponse(response_data_put, status=400)

        except Exception or ValueError or KeyError as e:
            response_data_put["details"] = str(e)
            return JSONResponse(response_data_put, status=400)

    elif request.method == 'DELETE':

        login_result = login(request, 'advertiser')
        login_result2 = login(request, 'admin')

        if login_result is not True and login_result2 is not True:
            return login_result

        if login_result is True:
            actor_aux = Actor.objects.get(user_account=request.user.id)
            if site.actor.id != actor_aux.id:
                return JSONResponse(response_site_not_belong, status=400)

        try:
            with transaction.atomic():
                # Remove site from db
                site.delete()

        except Exception or KeyError or ValueError as e:
            response_data_delete["details"] = str(e)
            return JSONResponse(response_data_delete, status=400)

        return HttpResponse(status=204)

    else:
        return JSONResponse(response_data_not_method, status=400)


def pruned_serializer_site_update(site, data):
    data["latitude"] = site.latitude
    data["longitude"] = site.longitude
    data["actor"] = site.actor.id

    return data
