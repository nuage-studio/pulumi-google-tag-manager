from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re

script_tag_template = '''
----------------------------------------------------------------------

Copy the following JavaScript and paste it as close to the opening <head> tag as possible on every page of your website

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','XXXXXXXX');</script>
<!-- End Google Tag Manager -->

------------------------------------------------------------------------

Copy the following snippet and paste it immediately after the opening <body> tag on every page of your website

<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=XXXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

------------------------------------------------------------------------
'''


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
            for p in properties.get('items'):
                if site_name == p.get('name'):
                    return p.get('id'), account

        web_property = service.management().webproperties().insert(
            accountId=account,
            fields='id',
            body={
                'websiteUrl': site_url,
                'name': site_name
            }
        ).execute()
        return web_property.get('id'), account
    else:
        raise "Google Analytics Account not available"


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
    ).execute()

    return web_property.get('id'), account_id


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
        webPropertyId=tracking_id
    )


def get_or_create_container(service, account_id, container_name):
    """Create or get container.

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
            'name': new_container_name,
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
    workspaces = service.accounts().containers().workspaces().list(
        parent=container['path']).execute()

    for ws in workspaces['workspace']:
        if ws['name'] == workspace_name:
            return ws

    return service.accounts().containers().workspaces().create(
        parent=container['path'],
        body={
            'name': workspace_name
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
            'name': new_workspace_name,
        }).execute()


def get_or_create_tag(service, workspace, tracking_id, tag_name):
    """Create the UA Tag.

    :service: the Tag Manager service object.
    :workspace: the workspace to create a tag within.
    :tracking_id: the tracking id to use.

    Returns:
      The created tag.
    """
    tags = service.accounts().containers().workspaces(
    ).tags().list(parent=workspace['path']).execute()

    if tags.get('tag'):
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
    return service.accounts().containers().workspaces().tags().update(
        path=tag['path'],
        body=tag_body
    ).execute()


def render_script_tag(container_id):
    return re.sub(r'XXXXXXXX', container_id, script_tag_template)
