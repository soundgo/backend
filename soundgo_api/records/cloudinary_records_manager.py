from cloudinary import config, uploader
import os

config(
    cloud_name="soundgo",
    api_key="228652582852825",
    api_secret="2rRo1h7nIeHkbvfKUqR8j0ApZwE"
)


def upload_record(base64):

    """
    Function to upload a record to the SoundGo Cloudinary repository
    :param base64: record in base64 format
    :return: secure URL where the record is uploaded
    """

    res = uploader.upload_large(base64, resource_type="video", folder="records/")
    return res["secure_url"]


def remove_record(url):

    """
    Function to remove a record of the SoundGo Cloudinary repository
    :param url: record URL
    :return: True if it is deleted correctly or False in another case
    """

    public_id = "/".join(os.path.splitext(url)[0].split("/")[-2:])
    res = uploader.destroy(public_id, resource_type="video")

    if res["result"] == "ok":
        return True
    else:
        return False
