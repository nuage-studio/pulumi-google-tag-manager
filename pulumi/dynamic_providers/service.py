from oauth2client.service_account import ServiceAccountCredentials
import pulumi


def get_key_file_location():
    config = pulumi.Config()
    return config.require("google_api_key_file")


def get_service(api_name, api_version, scopes):
    """Create a google service

    :api_name: the Tag Manager service object.
    :api_version: the path of the Tag Manager account from which to retrieve the container
    :scopes: name of the container
    :key_file_location: location of key file

    Returns:
      The google api service
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        get_key_file_location, scopes=scopes
    )
    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)
    return service
