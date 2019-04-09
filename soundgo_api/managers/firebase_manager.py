import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "soundgo-aec9e",
  "private_key_id": "7115972ec46c0fe05a9bf2865ab00bf4c3e8e753",
  "private_key": "-----BEGIN PRIVATE KEY-----\n"
                 "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3/uXHuGQYWesX\n"
                 "lHevHtd+tqVirOYZeQ8JlA6cgBc+4icQpGrje1KRoGUtp5sZCw/dngeO5el83NAR\n"
                 "sd6QZBDnVaUg1UQd/eDiMnAtcxg4ioKhoVU/Nif0ejhCuvpm919G90fT7yDAv5CS\n"
                 "614F9bE/zAptzbfPRoK8AtKg6ffUdKZLTuCt6ivNVQiW0NRYcZt+f9WHHfwSNeZx\n"
                 "d+smFOB8snC5fc+fMlPPgvQO3Yk6mP6demI+A9JdZW7v8cKET/LqrXpr8c0sa8ND\n"
                 "Xwnt090ArztB/3afIFXAQc7vhby5xcXKJRNFd8P9VCfCl4Cwc8wlP+SU8NPFccwC\n"
                 "HA6BikdZAgMBAAECggEABCbmesGmkZWa3Fz7b+pVYMzAkefWp+m/TP8oLsAltiOu\n"
                 "j720E0bNw88/pT54XaHuJVk68K6vvINzlwihXfcCGiRIvgNN/pLDa7tJZH8pw2Hd\n"
                 "xYWxWaQwVeAZq6jSPHdV0TFEj8vgPHU+LxCMXjxPeAHz1Ms8+/qKefFi3SJ2dxby\n"
                 "engMdRvGVr2ddAHv80OUiZ+RO35G/DC18PSGXBc5jkQoMRPd53pcB6K966CE5RuH\n"
                 "d9vQcNSk5dkHblxyREj3H+EQphnRYk88cI6zfBa22u8hIxbWI3Hr4FLLPAsZmm9r\n"
                 "asOs3Z5sOLIlBY9lsfeR9yQh/NHuxvJB8Z99YMoTYQKBgQDf5bLNnUeczjM1/SQl\n"
                 "RtkqOQ1YtvnKRLSGKjaLJPt2+cO7j3Qgrui/T7QDwajVuzSXtue7xBconvzbGvol\n"
                 "hPoDt94hrCGwC9GXWMbdbT96blPySIc4+HBwCdygu5YdvE+jsjpVaaj22V+1qZfv\n"
                 "3NiT8b3ae37mafd/AwV1gNYgYQKBgQDSYJW/TGcFDR5IoulMpUUggSDky41smVhq\n"
                 "AiY1P8UmWTL2H9YO3YvmP6tbITnj93QOB+lYcinQ43Gjidxvc9aRFAH/HgfmOyy0\n"
                 "Ztvv3ZE2xa9LGbcJ0o8J08smkjhXxemelrM3rF7aGk5K5bVeLHihx7CrOYE66FBd\n"
                 "EpLzkx1p+QKBgQCjLbGHEZ3jtpS0QG5bjKsxjqsfgRvEQxaewZ1HBAkRyS7SP9cP\n"
                 "Cusuo1Q7eKUoQGwwNmnl+yA1xsnalmrBdY0RsKwANofG2pZCi71EHB8rh8U+y4Vi\n"
                 "DA9GWKmnq4/Y1Cnm0DqbjYpLflm2+Id3lalzCbiox2DRZWGv+++6l893gQKBgF4O\n"
                 "ysTVrvWmMNT+6VnYRnjK4t8IVvmn8cyrm1ORaF7F4LAD+dt5mBPggYdj6pMOzrd7\n"
                 "OAvQNvvqxKL+fyzhWJxSmrXqQlPgPxOFLW4n3MXlSoNEQv7EQil9pMVg+IndtZ6u\n"
                 "9/+7NElFG54G57jsHx8NveI/+pRQy6VhKYx3SN5ZAoGAe/k1xCSWJEcPvweOiq56\n"
                 "walqF54cKj2XR4rUlkLjcNoaseUiiSBhieXPd64eKKlJ5Iej7Nt7wyaFNXkoyv83\n"
                 "N5YzEffB5WIEjLp4jdBv/VoPdznZx2NL+ySbuH/CIlSFd06p4UkPe0lxF41myfUB\n"
                 "+uyzidt7yg+0Ra9fSH9wflE=\n"
                 "-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-v1k4e@soundgo-aec9e.iam.gserviceaccount.com",
  "client_id": "100421721848078446078",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-v1k4e%40soundgo-aec9e."
                          "iam.gserviceaccount.com"
})

firebase_admin.initialize_app(cred)

db = firestore.client()

# #################### #
# ###### AUDIOS ###### #
# #################### #


def add_audio(audio):

    audio_id = audio.id
    audio_category = audio.category.name
    audio_latitude = audio.latitude
    audio_longitude = audio.longitude
    audio_actor = audio.actor.id
    audio_is_inappropriate = audio.isInappropriate
    audio_timestamp_creation = audio.timestampCreation
    audio_timestamp_finish = audio.timestampFinish
    audio_number_reproductions = audio.numberReproductions
    audio_duration = audio.duration
    audio_path = audio.path

    if audio.site:
        audio_site = audio.site.id
    else:
        audio_site = None

    data = {
        u'geometry': {
            u'coordinates': {
                u'0': audio_longitude,
                u'1': audio_latitude
            },
            u'type': u'Point'
        },
        u'properties': {
            u'id': audio_id,
            u'actorId': audio_actor,
            u'type': audio_category,
            u'tags': [],
            u'site': audio_site,
            u'isInappropriate': audio_is_inappropriate,
            u'timestampCreation': audio_timestamp_creation,
            u'timestampFinish': audio_timestamp_finish,
            u'numberReproductions': audio_number_reproductions,
            u'duration': audio_duration,
            u'path': audio_path
        },
        u'type': u'Feature'
    }

    db.collection(u'audios').add(data)


def update_audio(audio, tags=None):

    audio_id = audio.id
    audio_category = audio.category.name
    audio_is_inappropriate = audio.isInappropriate
    audio_timestamp_finish = audio.timestampFinish
    audio_number_reproductions = audio.numberReproductions

    collection = db.collection(u'audios')

    documents = collection.where(u'properties.id', u'==', int(audio_id)).get()

    if tags:
        for doc in documents:
            collection.document(doc.id).update({u'properties.tags': tags,
                                                u'properties.type': audio_category,
                                                u'properties.isInappropriate': audio_is_inappropriate,
                                                u'properties.timestampFinish': audio_timestamp_finish,
                                                u'properties.numberReproductions': audio_number_reproductions})
    else:
        for doc in documents:
            collection.document(doc.id).update({u'properties.type': audio_category,
                                                u'properties.isInappropriate': audio_is_inappropriate,
                                                u'properties.timestampFinish': audio_timestamp_finish,
                                                u'properties.numberReproductions': audio_number_reproductions})


def remove_audio(audio):

    audio_id = audio.id

    collection = db.collection(u'audios')

    documents = collection.where(u'properties.id', u'==', int(audio_id)).get()

    for doc in documents:
        collection.document(doc.id).delete()

# ############################ #
# ###### ADVERTISEMENTS ###### #
# ############################ #


def add_advertisement(advertisement):

    advertisement_id = advertisement.id
    advertisement_latitude = advertisement.latitude
    advertisement_longitude = advertisement.longitude
    advertisement_radius = advertisement.radius
    advertisement_actor = advertisement.actor.id
    advertisement_number_reproductions = advertisement.numberReproductions
    advertisement_duration = advertisement.duration
    advertisement_path = advertisement.path
    advertisement_max_price_to_pay = advertisement.maxPriceToPay
    advertisement_is_active = advertisement.isActive
    advertisement_is_delete = advertisement.isDelete

    data = {
        u'geometry': {
            u'coordinates': {
                u'0': advertisement_longitude,
                u'1': advertisement_latitude
            },
            u'type': u'Point'
        },
        u'properties': {
            u'id': advertisement_id,
            u'actorId': advertisement_actor,
            u'radius': advertisement_radius,
            u'numberReproductions': advertisement_number_reproductions,
            u'duration': advertisement_duration,
            u'path': advertisement_path,
            u'maxPriceToPay': advertisement_max_price_to_pay,
            u'isActive': advertisement_is_active,
            u'isDelete': advertisement_is_delete
        },
        u'type': u'Feature'
    }

    db.collection(u'ads').add(data)


def update_advertisement(advertisement):

    advertisement_id = advertisement.id
    advertisement_number_reproductions = advertisement.numberReproductions
    advertisement_max_price_to_pay = advertisement.maxPriceToPay
    advertisement_is_active = advertisement.isActive
    advertisement_is_delete = advertisement.isDelete

    collection = db.collection(u'ads')

    documents = collection.where(u'properties.id', u'==', int(advertisement_id)).get()

    for doc in documents:
        collection.document(doc.id).update({u'properties.numberReproductions': advertisement_number_reproductions,
                                            u'properties.maxPriceToPay': advertisement_max_price_to_pay,
                                            u'properties.isActive': advertisement_is_active,
                                            u'properties.isDelete': advertisement_is_delete})


def remove_advertisement(advertisement):

    advertisement_id = advertisement.id

    collection = db.collection(u'ads')

    documents = collection.where(u'properties.id', u'==', int(advertisement_id)).get()

    for doc in documents:
        collection.document(doc.id).delete()

# ################### #
# ###### SITES ###### #
# ################### #


def add_site(site):

    site_id = site.id
    site_name = site.name
    site_description = site.description
    site_latitude = site.latitude
    site_longitude = site.longitude
    site_actor = site.actor.id

    data = {
        u'geometry': {
            u'coordinates': {
                u'0': site_longitude,
                u'1': site_latitude
            },
            u'type': u'Point'
        },
        u'properties': {
            u'id': site_id,
            u'actorId': site_actor,
            u'name': site_name,
            u'description': site_description
        },
        u'type': u'Feature'
    }

    db.collection(u'sites').add(data)


def update_site(site):

    site_id = site.id
    site_name = site.name
    site_description = site.description

    collection = db.collection(u'sites')

    documents = collection.where(u'properties.id', u'==', int(site_id)).get()

    for doc in documents:
        collection.document(doc.id).update({u'properties.name': site_name,
                                            u'properties.description': site_description})


def remove_site(site):

    site_id = site.id

    collection = db.collection(u'sites')

    documents = collection.where(u'properties.id', u'==', int(site_id)).get()

    for doc in documents:
        collection.document(doc.id).delete()
