from pulumi import ComponentResource, Input, Output
from pulumi.dynamic import Resource, ResourceProvider, CreateResult, UpdateResult
from typing import Optional
import pulumi
from .api_wrapper import *
import json

tag_manager_scope = [
    'https://www.googleapis.com/auth/tagmanager.edit.containers',
    'https://www.googleapis.com/auth/tagmanager.delete.containers',
]
analytics_scope = ['https://www.googleapis.com/auth/analytics.edit']


class GTagManagerProvider(ResourceProvider):
    def create(self, props):

        analytics_service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=analytics_scope,
            key_file_location=props['key_file']
        )
        tag_manager_service = get_service(
            api_name='tagmanager',
            api_version='v2',
            scopes=tag_manager_scope,
            key_file_location=props['key_file']
        )

        # get tracking id
        tracking_id, account_id = get_or_create_tracking_id(
            service=analytics_service,
            site_name=props['site_name'],
            site_url=props['site_url'])

        # create container
        container = get_or_create_container(
            service=tag_manager_service,
            account_id=props['account_id'],
            container_name=props['container_name']
        )

        # create workspace
        container_ws = get_or_create_workspace(
            service=tag_manager_service,
            container=container,
            workspace_name=props['workspace_name']
        )

        # create tag
        tag = get_or_create_tag(
            service=tag_manager_service,
            workspace=container_ws,
            tracking_id=tracking_id,
            tag_name=props['tag_name']
        )

        # create script tag
        script_tag = render_script_tag(container['publicId'])
        
        return CreateResult(
            id_=props['account_id'],
            outs={
                **props,
                'script_tag': script_tag,
                'container_id': container['publicId']
            }
        )

    def update(self, id, _olds, props):
        # get traking id
        analytics_service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=analytics_scope,
            key_file_location=props['key_file']
        )


        tag_manager_service = get_service(
            api_name='tagmanager',
            api_version='v2',
            scopes=tag_manager_scope,
            key_file_location=props['key_file']
        )

        # get tracking id
        tracking_id, account_id = get_or_create_tracking_id(
            service=analytics_service,
            site_name=_olds['site_name'],
            site_url=_olds['site_url'])

        

        tracking_id, account_id = update_tracking_id(
            service=analytics_service,
            account_id=account_id,
            tracking_id=tracking_id,
            site_name=props['site_name'],
            site_url=props['site_url']
        )

        # get and update container
        container = get_or_create_container(
            service=tag_manager_service,
            account_id=_olds['account_id'],
            container_name=_olds['container_name']
        )

        container = update_container(
            service=tag_manager_service,
            container=container,
            new_container_name=props['container_name']
        )
        # # create workspace
        workspace = get_or_create_workspace(
            service=tag_manager_service,
            container=container,
            workspace_name=_olds['workspace_name']
        )

        workspace = update_workspace(
            service=tag_manager_service,
            workspace=workspace,
            new_workspace_name=props['workspace_name']
        )

        # # create tag
        tag = get_or_create_tag(
            service=tag_manager_service,
            workspace=workspace,
            tracking_id=tracking_id,
            tag_name=_olds['tag_name']
        )

        tag = update_tag(
            service=tag_manager_service,
            tag=tag,
            tracking_id=tracking_id,
            tag_name=props['tag_name']
        )

        # create script tag
        script_tag = render_script_tag(container['publicId'])

        return UpdateResult(
            outs={
                **props,
                'script_tag': script_tag,
                'container_id': container['publicId']
            }
        )

    def delete(self, id, props):
        analytics_service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=analytics_scope,
            key_file_location=props['key_file']
        )
        tag_manager_service = get_service(
            api_name='tagmanager',
            api_version='v2',
            scopes=tag_manager_scope,
            key_file_location=props['key_file']
        )

        # delete tracking id
        tracking_id, account_id = get_or_create_tracking_id(
            service=analytics_service,
            site_name=props['site_name'],
            site_url=props['site_url']
        )
        delete_tracking_id(
            service=analytics_service,
            account_id=account_id,
            tracking_id=tracking_id
        )

        # delete container
        container = get_or_create_container(
            service=tag_manager_service,
            account_id=props['account_id'],
            container_name=props['container_name']
        )
        delete_container(tag_manager_service, container)


class GTagManagerArgs(object):
    account_id: Input[str]
    container_name: Input[str]
    workspace_name: Input[str]
    tag_name = Input[str]
    site_name: Input[str]
    site_url: Input[str]
    key_file: Input[str]

    def __init__(self, account_id, container_name, workspace_name, tag_name, site_name, site_url, key_file):
        self.account_id = account_id
        self.container_name = container_name
        self.workspace_name = workspace_name
        self.tag_name = tag_name
        self.site_name = site_name
        self.site_url = site_url
        self.key_file = key_file


class GTagManager(Resource):
    container_id: Output[str]
    script_tag: Output[str]

    def __init__(self, name, args: GTagManagerArgs, opts=None):
        full_args = {
            'container_id': None,
            'script_tag': None,
            **vars(args)
        }
        super().__init__(GTagManagerProvider(), name, full_args, opts)
