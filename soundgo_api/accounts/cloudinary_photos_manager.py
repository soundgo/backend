from cloudinary import config, uploader
import os

config(
    cloud_name="soundgo",
    api_key="228652582852825",
    api_secret="2rRo1h7nIeHkbvfKUqR8j0ApZwE"
)


def upload_photo(base64):

    """
    Function to upload a photo to the SoundGo Cloudinary repository
    :param base64: photo in base64 format
    :return: secure URL where the photo is uploaded
    """

    res = uploader.upload(base64, folder="photos/")
    return res["secure_url"]


def remove_photo(url):

    """
    Function to remove a photo of the SoundGo Cloudinary repository
    :param url: photo URL
    :return: True if it is deleted correctly or False in another case
    """

    public_id = "/".join(os.path.splitext(url)[0].split("/")[-2:])
    res = uploader.destroy(public_id)

    if res["result"] == "ok":
        return True
    else:
        return False
