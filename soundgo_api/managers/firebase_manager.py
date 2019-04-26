import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "soundgo-a0f55",
  "private_key_id": "9bcefd4dc0e2dd6c95eceba3ac48b9b1ebd14b25",
  "private_key": "-----BEGIN PRIVATE KEY-----\n"
                 "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDbxjKmEmaZwvgF\n"
                 "Kv7XfSbw9zj0V2TRLS4xcCuGZ3aaD/oUKQzIGfS20roqKFDfGGk5TvJaXA+qAvco\n"
                 "HQ20gzbWW2jvIk4QxpYKtuExMBXJ1dUwnY4b+6715WQBJIGls4QrmG91/4Lck3Gq\n"
                 "qexpMjb7bvFEST8tBxvzOWigSGH6QjyaaZcbdDYlWzkgfNcQGvLuPzzePZoS/f+L\n"
                 "QSF/pKZQVkg/CZJLctikJuCzXXL1aseOUZ+Hr7BKDPSsZzEfBb7b/A5XPEDHoH2s\n"
                 "X+tU/HTi3JRUv5ujFiyI3d1UpJ6KR9HZFpTXM+CNncZ6KNViD2r24tQTpSPthxMR\n"
                 "F/HUflQ5AgMBAAECggEAArdMFHEpRfCwI9DgdeAffVOyJz42P38ysTHiQ9FfA0U7\n"
                 "xrMsK9k675B39FdBCpobYMsuOQ98B71CJIOEEhfws0z4EBkpLvwOn3gbnSyWNFiZ\n"
                 "aiCkVd8HeOqlEKjiFkll59ZaLZ04VuABRAXrZ0W+LV91Xq3rYzPRigZgBI0THZEy\n"
                 "nFF4zmlyY3YAXVIMStro1AAZnBA4XlVhWBVc0cdzxHotP1DPaITVxwXqw9nKUqsi\n"
                 "cO05l+z+g4yhV6ipuGzlAqFtipgabC4s344d1WhBwu3J56RDv6ngVWJ/Hv/5pIqN\n"
                 "MurSu1RChF0XjJ4lslAVDeNVN08UNLL+2xLsVy1XFQKBgQD+1URaal+CFXmeEkuv\n"
                 "Dp+He+h1Emvq8zI/BysncMd1H62C55rNXO/9HjNO3osMeTfO3O+4Hjyn+4uFnlQr\n"
                 "OiyF9cIcOu0iaH+8cs3VjokPSAYEGo+Dqpmij1kNOAtWgLnB5ynyqpal0b9aXSG0\n"
                 "Yc8YMXnAgLj5VHcSe3eS1v1JBQKBgQDcx9UY5+TND8jLtZXELk1K+KuPnRe+fWjD\n"
                 "IpaZoneplj6aCmwXPvuB08Bg8Dl3l8prR5L+4tLMSj7hTmUwlvodeKT9j8PTm4w0\n"
                 "p1VTvv6GZG4Lpyf9O1MbV6+WZst+SvmjfHC1aDmAZBGntSIAe8cK5fMr3g6JH7PS\n"
                 "GTZ1Pgh0pQKBgEsIvsykn6Ss8Bd0KabM9notKOA34WDX5Qab9L/zPDencS6nRXSM\n"
                 "lfmAx/jEHEs68gzODyO2e4O21HkuingD9BIpr9MiIqrL/Dif0S29f2vpeCQDMhjB\n"
                 "xeUQslbrFqOM2aVXjIlwY1VF8kMIQyFa32CvSLs+67g2f60If8fT19aFAoGAMY7t\n"
                 "x6xuEJXFdeyp1KKsGPMe15rktI7EEGFYOt5cTAX8wWkrgEBUBn14xonF7JF3D4O+\n"
                 "fFaACPl1ie+mCTUqqajmKEC4LWzSGROitKy/x30NsrHv6QkDC7UwJeunLA86YDdT\n"
                 "uXTOy4Iq8GFZY5BlSo35etRaoO8r1zJvpfupvD0CgYB6Y15p14VXXoiVrVq1fuio\n"
                 "9l7G1LM6HxLU8r3f+gJQWWlMOczLMUn5D+dPraIuLEpXscKs1Jp5K06Yia6aWizN\n"
                 "iyblnnfTWWHdtKLWirbJLCu+ZGoaJyH615dsJJhY30JZ+Abkx0GwRBPVhVPZM1Bp\n"
                 "dY9g+lonYDo3DH5XSYbm+g==\n"
                 "-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-8rpty@soundgo-a0f55.iam.gserviceaccount.com",
  "client_id": "106483786662850673080",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-8rpty%40soundgo-a0f55."
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
