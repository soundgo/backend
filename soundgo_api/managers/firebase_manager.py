import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "soundgo-94882",
  "private_key_id": "12956938c57fe1fcd527e3baf6751fafaa594241",
  "private_key": "-----BEGIN PRIVATE KEY-----\n"
                 "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDuhJm+h9/R3fi6\n"
                 "5YyNGucZKIeX6GUC2kpA10ApO8F1Mr+nMFCzH/hU6zMgOyKoBwymqpqqWEB7HfRR\n"
                 "0HbMTVeE8wIodC+mRHfQdk9w9U+OgMSBm/P7WXeWz6nlKwNTSLMIXXhHduBq9FT9\n"
                 "fyoLIDtHwDYLEWBZ0ME0hiSVqKehSv6TGenr9haia6l+fWbz+mA1WP8D7AcvY1m4\n"
                 "buhErufl9aMMwB2yk6S4/geFxKIaa7pdvYe0tha4eIUO9yieLwMFcPXd1hMD5mdh\n"
                 "6h7u0t1FkhlAGnn48clBFKJ5TSIaDUH5yO9q9ptKZXJ1aWNMdNmg2r6zdL2gUdqM\n"
                 "rECSHjwnAgMBAAECggEAXBa4IVbmdGnGOaqc7HHhndYHHABu134eQxCYRhM7Kxuv\n"
                 "4UYHMlF6mJbCg4QxajxmhwbBdllic+ZpyRi6dUC7NKp6P9Iz/3bZ55N2Mn+T+sn+\n"
                 "lKf4uCefw4tj5gYIX6Rm8yjbYoQkO0cgdUsemXMVUCuG8hkAYUz2+2d7Qoj+R4gl\n"
                 "Cxz7aUBX5vxgDJKnJqXnTnNTaR3rdLRdNHq0Mo22n0p7z09ZLGky9GmKit/4uoTH\n"
                 "H4Z5RqScR5GW4MG89v7oMFj0DMwfOmhE133+HOYtL8W8u/QBzwWoO+PtrGaZX0qG\n"
                 "4+fJxiKw782vQyz62hYAGWTsirB8IaZqm3NNoFeVIQKBgQD88fRhSy00jlGl3Dkp\n"
                 "5Dca0LigSfPzuKZM/rJx6cIkoC+9P/HNqepAcU2+opMmH2w5UEQyERFGIrkuh2O2\n"
                 "oHCITBmcxmDg/yXOHGKPViP3RdzGjcNMiTd2h/nTfkKYCpm5PzcqyKy+Sqoa+Y9O\n"
                 "UVEOOZ7cHLgTTLpv0Eus34zg0QKBgQDxZgpnWYKgYhA1yUWlyyqZrWeKyHvwrIjN\n"
                 "8uPiBY4p3NrRwnRIh3gYnbjGDjJzD+U7n8Z7RlKAJmWaO0jiDc/O/8l8/ZiV8Uql\n"
                 "1v0eZOjewV2kBfQCZZXjS3s2F/bISIjZfc7E3g6qb/pSXaYox7HHqnvgz+PH6yJW\n"
                 "BuSEUpzLdwKBgAfP0SRQFg1Rd+QPcRSCH9GMMKeCoS4dvcUS+J/cAErxR4gouWcI\n"
                 "oFttJGGG09SRk94RRInnTQlFeUKem83AFrme4AufdM5+EsTSy5hxqJqyZaccKbPr\n"
                 "aPMYL/cAJz5a1XSLJ0EDAZK+65H5sxtQF5jA3s8dc/HkpL1fSXcFUGyBAoGBAO5e\n"
                 "78kMR4QuMYmbPY4w59kmtUcDH/gRt2l+/m4zRCWsc9uL5B22v+222T2hyUl7mcXd\n"
                 "yTXzxAXNZKj+/8JRFzJ1vLYTCTiPM0I94GbCCH3mfZw5ULGJNJBk+b75vPQbRB9Y\n"
                 "LvSRvfOpbYsl9KzyPGhIvdjKEEhatOY0GjVcCn6TAoGAQRHLYfBzlJ7ve1mTLS9e\n"
                 "QekVbS1JG8m9srZSOAKLFyETxz4CI0KptSb+Qh9d4KBjQiR1PFyrESnMOyazcjen\n"
                 "xi/NJqe2k5bio6Igzr09K5LLKopp/K90dBvL8cCkGdVYkTNDLTZtQIPH0691GCBW\n"
                 "pKocm5QWtNYQmtWT22YFDwQ=\n"
                 "-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ew2jf@soundgo-94882.iam.gserviceaccount.com",
  "client_id": "111393030509917214219",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ew2jf%40soundgo-94882."
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
