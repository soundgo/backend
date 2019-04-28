from django.test import TestCase

import json

from .models import Site
from . import views

from configuration.models import Configuration

from accounts.views import get_token
from accounts.models import Actor, CreditCard

from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory


class SitesTest(TestCase):

    def setUp(self):
        configuration = Configuration.objects.create(maximum_radius=20000, minimum_radius=20,
                                                     time_listen_advertisement=3.0, minimum_reports_ban=10,
                                                     time_extend_audio=3600)
        configuration.save()

        UserAccount = get_user_model()
        user_account = UserAccount.objects.create_user_account('carlos', 'Carlos123.',
                                                               is_active=True)
        credit_card = CreditCard.objects.create(holderName='Carlos Mallado', brandName='MASTERCARD',
                                                number='5364212315362996', expirationMonth=7, expirationYear=21,
                                                cvvCode=841, isDelete=False)
        actor = Actor.objects.create(user_account=user_account, email='soundgoapp2@gmail.com',
                                     photo='',
                                     credit_card=credit_card)
        actor.save()

    def tearDown(self):
        Configuration.objects.all().delete()
        Actor.objects.all().delete()
        Site.objects.all().delete()

    # Test cases
    def test_crud_site(self):

       # Create site
        site= self.create_site({"name": "Escuela informática", "description": "Aprende informática en tu lugar  favorito", "longitude": 35.23, "latitude": -5.34}, 201)

        # Update site
        self.update_site({"name": "Escuela informática II", "description": "Aprende informática en tu lugar  favorito reformado"}, 200, site['id'])

        # Get site
        self.get_site(200, site['id'])

        # Delete site
        self.delete_site(204, site['id'])

        # Site deleted can not get again
        self.get_site(404, site['id'])

        # Site deleted can not delete again
        self.delete_site(404, site['id'])

        # Site deleted can not update again
        self.update_site(
            {"name": "Escuela informática II", "description": "Aprende informática en tu lugar  favorito reformado"},
            404, site['id'])

    #Auxiliary methods
    def create_site(self, object, code):

        token = self.get_token("carlos", "Carlos123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        request = factory.post('/site/', body, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)

        response = views.site_create(request)

        self.assertTrue(response.status_code == code)

        return json.loads(response.getvalue().decode())

    def update_site(self, object, code, id):

        token = self.get_token("carlos", "Carlos123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        request = factory.put('/sites/site/' + str(id) + "/", body, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)

        response = views.site_update_delete_get(request,id)

        self.assertTrue(response.status_code == code)

        return json.loads(response.getvalue().decode())

    def delete_site(self, code, id):

        token = self.get_token("carlos", "Carlos123.")

        factory = APIRequestFactory()

        request = factory.delete('/sites/site/' + str(id) + "/", content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)

        response = views.site_update_delete_get(request,id)

        self.assertTrue(response.status_code == code)

    def get_site(self, code, id):

        factory = APIRequestFactory()
        request = factory.get('/sites/site/' + str(id) + "/", content_type='application/json')
        response = views.site_update_delete_get(request,id)

        self.assertTrue(response.status_code == code)

    def get_token(self, username, password):
        body = json.dumps({"nickname": username, "password": password})

        factory = APIRequestFactory()
        request = factory.post('/api-token-auth/', body, content_type='application/json')
        response = get_token(request)

        r = json.loads(response.getvalue().decode())
        return r['token']
