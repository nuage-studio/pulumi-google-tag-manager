from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Create a google service

    :api_name: the Tag Manager service object.
    :api_version: the path of the Tag Manager account from which to retrieve the container
    :scopes: name of the container
    :key_file_location: location of key file

    Returns:
      The google api service
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes)
    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)
    return service


def get_or_create_tracking_id(service, site_name, site_url):
    """Creates or get google analytics tracking id.

    :service: the google analytics service object.
    :site_name: name of the site
    :site_url: url of the site

    Returns:
      The google analytics tracking id
    """
    accounts = service.management().accounts().list(fields='items').execute()

    if accounts.get('items'):

        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account, fields='items').execute()

        if properties.get('items'):

          # check if property already exists then simply return tracking code from property
            for property in properties.get('items'):
                if site_name == property.get('name'):
                    return property.get('id')

            web_property = service.management().webproperties().insert(
                accountId=account,
                fields='id',
                body={
                    'websiteUrl': site_url,
                    'name': site_name
                }
            ).execute()
    return web_property.get('id'), account_id


def update_tracking_id(service, account_id, tracking_id, site_name, site_url):
    """Updates the tracking id.

    :service: the google analytics service object.
    :account_id: Google analytics account id
    :tracking_id: google analytics tracking id
    :site_name: name of the site
    :site_url: url of the site

    Returns:
      The updated tracking id.
    """
    web_property = service.management().webproperties().update(
        accountId=account_id,
        webPropertyId=tracking_id,
        body={
            'websiteUrl': site_url,
            'name': site_name
        }
    )
    return web_property.get('id')


def delete_tracking_id(service, account_id, tracking_id):
    """Deletes the tracking id.

    :service: the google analytics service object.
    :account_id: Google analytics account id
    :tracking_id: google analytics tracking id

    Returns:
      None
    """
    service.management().webproperties().update(
        accountId=account_id,
        webPropertyId=tracking_id,
        body={
            'websiteUrl': site_url,
            'name': site_name
        }
    )


def get_or_create_container(service, account_id, container_name):
    """Find the container.

    :service: the Tag Manager service object.
    :account_path: the path of the Tag Manager account from which to retrieve the container
    :container_name: name of the container

    Returns:
      The container object
    """
    # Query the Tag Manager API to list all containers for the given account.
    account_path = f'accounts/{account_id}'
    container_wrapper = service.accounts().containers().list(
        parent=account_path).execute()

    # Find and return the Greetings container if it exists.
    for container in container_wrapper['container']:
        if container['name'] == container_name:
            return container
    return service.accounts().containers().create(
        parent=account_path,
        body={
            'name': container_name,
            'usage_context': ['web']
        }).execute()


def update_container(service, container, new_container_name):
    """Updates the container.

    :service: the Tag Manager service object.
    :container: the container object to be updated
    :new_container_name: new container name

    Returns:
      The updated container.
    """
    return service.accounts().containers().update(
        path=container['path'],
        body={
            'name': container_name,
            'usage_context': ['web']
        }).execute()


def delete_container(service, container):
    """Deleted the Container.

    :service: the Tag Manager service object.
    :container: the container to be deleted

    Returns:
      None
    """
    service.accounts().containers().delete(
        path=container['path']
    ).execute()


def get_or_create_workspace(service, container, workspace_name):
    """Get or Create a workspace.

    :service: the Tag Manager service object.
    :container: the container object to insert the workspace within.
    :workspace_name: name of the workspace

    Returns:
      The workspace object.
    """
    workspaces = service.accounts().containers().list(
        parent=conatiner['path']).execute()

    # Find and return the Greetings container if it exists.
    for workspace in workspaces['workspace']:
        if workspace['name'] == workspace_name:
            return workspace

    return service.accounts().containers().workspaces().create(
        parent=container['path'],
        body={
            'name': workspace_name,
        }).execute()


def update_workspace(service, workspace, new_workspace_name):
    """Updates the Workspace.

    :service: the Tag Manager service object.
    :workspace: the workspace object
    :new_workspace_name: new workspace name

    Returns:
      The updated workspace.
    """
    return service.accounts().containers().workspaces().update(
        path=workspace['path'],
        body={
            'name': workspace_name,
        }).execute()


def get_or_create_tag(service, workspace, tracking_id, tag_name):
    """Create the UA Tag.

    :service: the Tag Manager service object.
    :workspace: the workspace to create a tag within.
    :tracking_id: the tracking id to use.

    Returns:
      The created tag.
    """
    tags = service.accounts().containers().workspace(
    ).tags().list(parent=workspace['path']).execute()

    for tag in tags['tag']:
        if tag['name'] == tag_name:
            return tag

    tag_body = {
        'name': tag_name,
        'type': 'ua',
        'parameter': [{
            'key': 'trackingId',
            'type': 'template',
            'value': str(tracking_id),
        }],
    }

    return service.accounts().containers().workspaces().tags().create(
        parent=workspace['path'],
        body=tag_body).execute()


def update_tag(service, tag, tracking_id, tag_name):
    """Updates the UA Tag.

    :service: the Tag Manager service object.
    :tag: the tag object
    :tracking_id: new tracking id
    :tag_name: new tag name

    Returns:
      The updated tag.
    """
    tag_body = {
        'name': tag_name,
        'type': 'ua',
        'parameter': [{
            'key': 'trackingId',
            'type': 'template',
            'value': str(tracking_id),
        }],
    }
    return service.accounts().containers().workspaces().tags.update(
        path=tag['path'],
        body=tag_body
    )
