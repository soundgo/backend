from requests import post, put, delete
from requests.exceptions import RequestException


def create_mapbox(category, latitude, longitude, idRecord):
    # Mapbox configuration
    datasetMap = {"site": "cjtke1edi02q02wn5kjd9en24", "leisure": "cjtkadw8e03jy4fnycl0ue5cn",
                  "experience": "cjtkae6lv0phe2xtg8u2jiny9", "tourism": "cjtkaesz804254bodwfnw63r6",
                  "advertisement": "cjtkacy841h2g2wllukp7sfij"}
    token = "sk.eyJ1Ijoic291bmRnbyIsImEiOiJjanRrYzl0a3YwZ3ljM3lxamVqYmhidjJmIn0.zwUJZmYb3qrhsLoPN-Xqrw"
    idDataset = datasetMap[category.lower()]

    url= "https://api.mapbox.com/datasets/v1/soundgo/"+idDataset+"/features/"+str(idRecord)+"?access_token="+token
    params= {
        "id": str(idRecord),
        "geometry": {
            "coordinates": [
              float(latitude),
              float(longitude)
            ],
            "type": "Point"
        },
        "type": "Feature",
        "properties": {

        }
    }

    try:
        request= put(url, json= params)
        response = request.text
    except RequestException:
        response = "Error saving record in mapbox"

    return response


def delete_mapbox(category, idRecord):
    # Mapbox configuration
    datasetMap = {"site": "cjtke1edi02q02wn5kjd9en24", "leisure": "cjtkadw8e03jy4fnycl0ue5cn",
                  "experience": "cjtkae6lv0phe2xtg8u2jiny9", "tourism": "cjtkaesz804254bodwfnw63r6",
                  "advertisement": "cjtkacy841h2g2wllukp7sfij"}
    token = "sk.eyJ1Ijoic291bmRnbyIsImEiOiJjanRrYzl0a3YwZ3ljM3lxamVqYmhidjJmIn0.zwUJZmYb3qrhsLoPN-Xqrw"
    idDataset = datasetMap[category.lower()]

    url = "https://api.mapbox.com/datasets/v1/soundgo/" + idDataset + "/features/" + str(idRecord) + "?access_token=" + token

    try:
        request = delete(url)
        response = request.text
    except RequestException:
        response = "Error deleting record in mapbox"

    return response


def update_mapbox():

    # Mapbox configuration
    datasetMap = {"site": "cjtke1edi02q02wn5kjd9en24", "leisure": "cjtkadw8e03jy4fnycl0ue5cn",
                  "experience": "cjtkae6lv0phe2xtg8u2jiny9", "tourism": "cjtkaesz804254bodwfnw63r6",
                  "advertisement": "cjtkacy841h2g2wllukp7sfij"}
    tilesetMap = {"site": "soundgo.sites", "leisure": "soundgo.leisure", "experience": "soundgo.experience",
                  "tourism": "soundgo.tourism", "advertisement": "soundgo.ads"}
    token = "sk.eyJ1Ijoic291bmRnbyIsImEiOiJjanRrYzl0a3YwZ3ljM3lxamVqYmhidjJmIn0.zwUJZmYb3qrhsLoPN-Xqrw"

    for key, value in datasetMap.items():
        idDataset = datasetMap[key]
        idTileset = tilesetMap[key]

        url = "https://api.mapbox.com/uploads/v1/soundgo?access_token="+token
        params = {
            "tileset": idTileset,
            "url": "mapbox://datasets/soundgo/"+idDataset,
            "name": idTileset.split(".")[1]
        }

        try:
            request = post(url, json=params)
            response = request.text
        except RequestException:
            response = "Error saving record in mapbox"

    return response
