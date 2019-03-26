import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "soundgo-ba26c",
  "private_key_id": "9312c03d54273af90f26c2518377cf68a9d8cd5b",
  "private_key": "-----BEGIN PRIVATE KEY-----\n"
                 "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDFmHKHVwltLNL9\n"
                 "MhdKDW8ak5yS1NZcKERcal2JOlDsk3Q74Nm/rb9obtyR9QVFNQCwDIuB/1XgHG0R\n"
                 "dLuN8YCTERohRbgUd0pE3dHJrI7B3dViI3Y33OjnPexqTnGjzjzquC8bscYVUbUJ\n"
                 "sXglH0EZxiQcQsVbKETAmIBVatq1lFyfr+WeIgebPSPALtpgj4EE7/JfbLUSIS6g\n"
                 "z+AdhuyyIAAGO7de0rKQj3lMETXpEL3mdipytFciM7/Sy+B+F5C8WSDu0bUt3Aly\n"
                 "wKmW/RhnjKoeifO5ScNy6FF9jV4RSBFGxTORSyhP4gUjxP0qZ5kiBVZIYZHAZZ4T\n"
                 "flqA9wFxAgMBAAECggEACgZKTi82W1d2M1IAoDlHARdKzuC1KNsCn9kmGm2O2DfB\n"
                 "Yn3NckXpc24HavC+NhUCrkvOopdehxaOGn/8eW6uhheMprI7rO8h4ZVK3MNQQUnk\n"
                 "ttxDdcFTgBLSTRDif0vZ55MVUb9+xAtfhsi+Bo0bv4ffwl7JVi74cPhzr1Gy25oe\n"
                 "1K+EPv1TAQvpYGTIlValW3Mw38kFVH9DfQb1P4PUweTmKPlBIALYw+ZV2kEJRptt\n"
                 "WL9Yob+6BrYkYcEEgZg/6koS3/VWVNRC5vbdyZp1pKgNVLx4PSXmtf38ZpA3X+28\n"
                 "eizrVibtmGosqdCmOaDdMTFbmQm8rRbWHwNlS17weQKBgQDo1sI+4Ln3VIo2oHhA\n"
                 "N0VbXEhN7MloV4z+46DyAxGkYcuZx/Yg2D9shZ6+NNr2k0Eq1aYtsnHB7MPuAGq7\n"
                 "YLM6O6Rd+MKpv0gC+ZGRGBmoqN3ZFPBcw/XcODZAF5BPJpur9avmCHXwIfxEE4SS\n"
                 "ErITbCGyW4zvPpAJydgX+EY0OQKBgQDZQDctc9KHiF9zMBTsXRvvT9sx147bsr86\n"
                 "Xu975HWDAWND05UCwEkWJuHGOCBZe7wUNkP2FWYkpXFGfMcpvsEqKPiBPj6ut3ng\n"
                 "jhY3ZuoKA/HGTaZ9Au0HbmIAQ1xHBomGK/dWXT4lJQgny510W9pNKaNnYFOmqy4K\n"
                 "VUswbdvm+QKBgEjmTITxSWhVsLxvu5and3CmUQEM3PZtSvjW/iInsdNcxylLwRUB\n"
                 "f8ITh+MXm2LOMf4eTFxMXW+RGLsgqEooeZUG7Wx6oUASYpKD3v6lpAr5bBQ2iRcS\n"
                 "R5z+gIXKmuUdOmo5jeuExKA9k8Ugs0Yk0lpgZaB5J4QUe3aFGsJOenSJAoGBALdF\n"
                 "1AaVGfraUeODoXMQzTsivACdH1g5v9bHNfLndTbyWcJjYOa0PjPg00B8ItY6ax0F\n"
                 "9mlH/iZWJ2xWYVHXKW+epp2pXAnaoIeOdjGAsVmHoFQxN41ohXtqZGRibxs/6Y51\n"
                 "0q9Z8840ImAoBomd31iPEtlnysnkyO9QqyCM3SFJAoGBAMNr7yAN5tjjL1hquoPb\n"
                 "mEfV9edjnqsijOGX5Znex7VA50htJyMY7bd+YBLGCfr97GRcXFV4TgUOsOIih5/Z\n"
                 "eykZvy0UHK/UhNN8leBsQp77sQWcX1HEIZ1lug/JdKDg/g5IPZ1qX02phVygueNZ\n"
                 "THjxQx3skU+siL6+69wZf4mL\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-b1xq0@soundgo-ba26c.iam.gserviceaccount.com",
  "client_id": "102756503705771459049",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-"
                          "adminsdk-b1xq0%40soundgo-ba26c.iam.gserviceaccount.com"
})

firebase_admin.initialize_app(cred)

db = firestore.client()


def add_audio(audio):

    audio_id = audio.id
    audio_category = audio.category.name
    audio_latitude = audio.latitude
    audio_longitude = audio.longitude

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
            u'type': audio_category
        },
        u'type': u'Feature'
    }

    db.collection(u'audios').add(data)


def add_advertisement(advertisement):

    advertisement_id = advertisement.id
    advertisement_latitude = advertisement.latitude
    advertisement_longitude = advertisement.longitude

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
        },
        u'type': u'Feature'
    }

    db.collection(u'ads').add(data)


def add_site(site):

    site_id = site.id
    site_name = site.name
    site_latitude = site.latitude
    site_longitude = site.longitude

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
            u'name': site_name
        },
        u'type': u'Feature'
    }

    db.collection(u'sites').add(data)


def remove_audio(audio):

    audio_id = audio.id

    collection = db.collection(u'audios')

    documents = collection.where(u'properties.id', u'==', int(audio_id)).get()

    for doc in documents:
        collection.document(doc.id).delete()


def remove_advertisement(advertisement):

    advertisement_id = advertisement.id

    collection = db.collection(u'ads')

    documents = collection.where(u'properties.id', u'==', int(advertisement_id)).get()

    for doc in documents:
        collection.document(doc.id).delete()


def remove_site(site):

    site_id = site.id

    collection = db.collection(u'sites')

    documents = collection.where(u'properties.id', u'==', int(site_id)).get()

    for doc in documents:
        collection.document(doc.id).delete()
