from pulumi import ComponentResource, Input, Output
from pulumi.dynamic import Resource, ResourceProvider, CreateResult, UpdateResult
from typing import Optional

tag_manager_scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers',
                     'https://www.googleapis.com/auth/tagmanager.delete.container',
                     ]
analytics_scope = ['https://www.googleapis.com/auth/analytics.edit']


class GTagManagerProvider(ResourceProvider):

    def create(self, props):
        # TO DO
        pass

    def update(self, id, _olds, props):
        # TO DO
        pass

    def delete(self, id, props):
        # TO DO
        pass


class GTagManagerArgs(object):
    account_id: Input[str]
    container_name: Input[str]
    workspace_name: Input[str]
    tag_name = Input[str]
    site_name: Input[str]
    site_url: Input[str]

    def __init__(self, account_id, container_name, workspace_name, tag_name, site_name, site_url):
        self.account_id = account_id
        self.container_name = container_name
        self.workspace_name = workspace
        self.tag_name = tag_name
        self.site_name = site_name
        self.site_url = site_url


class GTagManager(Resource):
    account_id: Output[str]
    container_name: Output[str]
    workspace_name: Output[str]
    tag_name = Output[str]
    site_name: Output[str]
    site_url: Output[str]

    def __init__(self, name, args: GTagManagerArgs, opts=None):
        full_args = {'site_name': None, 'site_url': None, **vars(args)}
        super().__init__(GTagManagerProvider(), name, full_args, opts)
