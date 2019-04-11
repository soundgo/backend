from django.test import TestCase

# Create your tests here.
# Create your tests here.
from django.test import TestCase
import requests
import json


class SitesTest(TestCase):


    def get_host(self):
        #return "http://127.0.0.1:8000"
        return "https://soundgo-api-v2.herokuapp.com"


    #Test cases
    def test_crud_site(self):

        #Create site
        site= self.create_site({"name": "Escuela informática", "description": "Aprende informática en tu lugar  favorito", "longitude": 35.23, "latitude": -5.34}, 201)

        #Update site
        self.update_site({"name": "Escuela informática II", "description": "Aprende informática en tu lugar  favorito reformado"}, 200, site['id'])

        #Get site
        self.get_site(200, site['id'])

        #Delete site
        self.delete_site(204, site['id'])

        #Site deleted can not get again
        self.get_site(404, site['id'])

        #Site deleted can not delete again
        self.delete_site(404, site['id'])

        #Site deleted can not update again
        self.update_site(
            {"name": "Escuela informática II", "description": "Aprende informática en tu lugar  favorito reformado"},
            404, site['id'])

    #########


    #Auxiliary methods
    def create_site(self, object, code):

        token = self.get_token("soundgoadvertiser", "soundgoadvertiser")

        headers = {'content-type': 'application/json', 'Authorization' : "Bearer "+token}
        body = json.dumps(object)

        r = requests.post(self.get_host() + '/sites/site/', data=body, headers=headers)


        self.assertTrue(r.status_code == code)

        return r.json()


    def update_site(self, object, code, id):

        token = self.get_token("soundgoadvertiser", "soundgoadvertiser")

        headers = {'content-type': 'application/json', 'Authorization' : "Bearer "+token}
        body = json.dumps(object)

        r = requests.put(self.get_host() + '/sites/site/'+str(id)+"/", data=body, headers=headers)


        self.assertTrue(r.status_code == code)

        return r.json()


    def delete_site(self, code, id):

        token = self.get_token("soundgoadvertiser", "soundgoadvertiser")

        headers = {'content-type': 'application/json', 'Authorization' : "Bearer "+token}

        r = requests.delete(self.get_host() + '/sites/site/'+str(id)+"/", headers=headers)

        self.assertTrue(r.status_code == code)


    def get_site(self, code, id):

        headers = {'content-type': 'application/json'}

        r = requests.get(self.get_host() + '/sites/site/' + str(id) + "/", headers=headers)

        self.assertTrue(r.status_code == code)


    def get_token(self, username, password):
        headers = {'content-type': 'application/json'}
        body = json.dumps({"nickname": username, "password": password})

        r = requests.post(self.get_host() + '/api-token-auth/', data=body, headers=headers)

        return r.json()['token']
