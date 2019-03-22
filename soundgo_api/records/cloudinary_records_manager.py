from cloudinary import config, uploader

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
